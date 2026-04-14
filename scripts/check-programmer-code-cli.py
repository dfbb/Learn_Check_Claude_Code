#!/usr/bin/env python3
"""
Claude Code / Codex 使用情况统计工具
统计过去 30 天内的使用数据，输出多维度报告和综合得分。
"""
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional


# ─── 工具分类 ────────────────────────────────────────────────────────────────

# 编码类工具：衡量实际编码工作量
CODE_TOOLS = {"Edit", "Write", "Read", "Glob", "Grep", "NotebookEdit"}

# 高级能力工具：衡量工具使用深度
ADVANCED_TOOLS = {"Agent", "WebSearch", "WebFetch", "LSP", "Bash", "Task",
                  "TaskCreate", "TaskUpdate", "TaskGet", "TaskList"}


# ─── 统计收集器 ───────────────────────────────────────────────────────────────

class StatsCollector:
    def __init__(self):
        # Token 统计
        self.total_input_tokens = 0
        self.total_cached_input_tokens = 0
        self.total_cache_read_input_tokens = 0
        self.total_output_tokens = 0

        # 会话与消息
        self.total_sessions = 0
        self.total_messages = 0

        # Skill 统计
        self.total_skill_uses = 0
        self.skill_counts = defaultdict(int)

        # 工具调用统计（按工具名）
        self.tool_counts = defaultdict(int)

        # 活跃日期集合（用于计算 streak）
        self.active_dates: set = set()

    # ── Token 提取 ────────────────────────────────────────────────────────────

    def _extract_tokens(self, obj: dict):
        """从 usage 对象中累加各类 token 数量"""
        self.total_input_tokens += obj.get('input_tokens', 0)
        self.total_cached_input_tokens += obj.get('cached_input_tokens', 0)
        self.total_cache_read_input_tokens += obj.get('cache_read_input_tokens', 0)
        self.total_output_tokens += obj.get('output_tokens', 0)

    # ── 时间工具 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_timestamp(ts) -> Optional[float]:
        """将各种格式的时间戳统一转为 Unix 时间戳（秒）"""
        try:
            if isinstance(ts, (int, float)):
                # 毫秒级时间戳自动转换
                return ts / 1000 if ts > 1e12 else float(ts)
            if isinstance(ts, str):
                return datetime.fromisoformat(ts.replace('Z', '+00:00')).timestamp()
        except Exception:
            pass
        return None

    def _record_date(self, ts_raw):
        """记录活跃日期（用于 streak 计算）"""
        ts = self._parse_timestamp(ts_raw)
        if ts:
            self.active_dates.add(datetime.fromtimestamp(ts).date())

    @staticmethod
    def _is_recent(ts_raw, cutoff_ts: float) -> bool:
        """判断时间戳是否在截止时间之后"""
        ts = StatsCollector._parse_timestamp(ts_raw)
        return ts is not None and ts >= cutoff_ts

    @staticmethod
    def _file_is_recent(file_path: str, cutoff_ts: float) -> bool:
        """通过文件修改时间快速过滤旧文件"""
        return os.path.getmtime(file_path) >= cutoff_ts

    # ── 工具调用统计 ──────────────────────────────────────────────────────────

    def _process_tool_calls(self, content: list):
        """
        从 message.content 数组中提取工具调用。
        同时处理 Skill 调用和 Agent 子类型。
        """
        for item in content:
            if not isinstance(item, dict) or item.get('type') != 'tool_use':
                continue
            name = item.get('name', '')
            if not name:
                continue

            inp = item.get('input', {}) or {}

            if name == 'Skill':
                # Skill 工具：记录具体 skill 名称
                skill_name = inp.get('skill', '')
                if skill_name:
                    self.skill_counts[skill_name] += 1
                    self.total_skill_uses += 1
            elif name == 'Agent':
                # Agent 工具：记录子类型
                agent_type = inp.get('subagent_type', 'unknown')
                self.tool_counts[f"Agent:{agent_type}"] += 1
            else:
                self.tool_counts[name] += 1

    # ── 文件处理：Codex sessions ──────────────────────────────────────────────

    def process_codex_session(self, file_path: str, cutoff_ts: float):
        """处理 ~/.codex/sessions/ 下的 JSONL 文件"""
        if not self._file_is_recent(file_path, cutoff_ts):
            return

        self.total_sessions += 1
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts = data.get('timestamp')
                    if ts and not self._is_recent(ts, cutoff_ts):
                        continue
                    if ts:
                        self._record_date(ts)

                    self.total_messages += 1

                    # Codex token_count 事件（优先用 last_token_usage 避免累计重复）
                    if data.get('type') == 'event_msg':
                        payload = data.get('payload', {})
                        if isinstance(payload, dict) and payload.get('type') == 'token_count':
                            info = payload.get('info', {})
                            if isinstance(info, dict):
                                usage = (info.get('last_token_usage')
                                         or info.get('total_token_usage')
                                         or info)
                                if isinstance(usage, dict):
                                    self._extract_tokens(usage)

                    # 通用 usage 字段
                    elif 'usage' in data and isinstance(data['usage'], dict):
                        self._extract_tokens(data['usage'])

                    # 工具调用
                    content = (data.get('message', {}) or {}).get('content', [])
                    if isinstance(content, list):
                        self._process_tool_calls(content)

        except Exception:
            pass

    # ── 文件处理：costs.jsonl ─────────────────────────────────────────────────

    def process_costs_jsonl(self, file_path: str, cutoff_ts: float):
        """处理 ~/.claude/metrics/costs.jsonl"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts = data.get('timestamp')
                    if ts and not self._is_recent(ts, cutoff_ts):
                        continue
                    if ts:
                        self._record_date(ts)

                    self._extract_tokens(data)
                    self.total_messages += 1
        except Exception as e:
            print(f"  ⚠ 处理 costs.jsonl 出错: {e}")

    # ── 文件处理：Claude projects ─────────────────────────────────────────────

    def process_claude_project_jsonl(self, file_path: str, cutoff_ts: float):
        """处理 ~/.claude/projects/ 下的 JSONL 文件"""
        if not self._file_is_recent(file_path, cutoff_ts):
            return

        session_counted = False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts = data.get('timestamp')
                    if ts and not self._is_recent(ts, cutoff_ts):
                        continue
                    if ts:
                        self._record_date(ts)

                    # 每个文件计为一个 session（首次有效行时计数）
                    if not session_counted:
                        self.total_sessions += 1
                        session_counted = True

                    # 统计 user/assistant 消息
                    msg_type = data.get('type', '')
                    if msg_type in ('user', 'assistant'):
                        self.total_messages += 1

                    # 提取 token 用量（优先从 message.usage）
                    msg = data.get('message')
                    if isinstance(msg, dict):
                        if 'usage' in msg:
                            self._extract_tokens(msg['usage'])
                        # 提取工具调用
                        content = msg.get('content', [])
                        if isinstance(content, list):
                            self._process_tool_calls(content)
                    elif 'usage' in data and isinstance(data['usage'], dict):
                        self._extract_tokens(data['usage'])

        except Exception:
            pass

    # ── Streak 计算 ───────────────────────────────────────────────────────────

    def compute_streak(self) -> tuple[int, int]:
        """
        返回 (总活跃天数, 最长连续天数)。
        连续天数：相邻日期差为 1 天。
        """
        if not self.active_dates:
            return 0, 0

        sorted_dates = sorted(self.active_dates)
        total_active = len(sorted_dates)

        max_streak = 1
        cur_streak = 1
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
                cur_streak += 1
                max_streak = max(max_streak, cur_streak)
            else:
                cur_streak = 1

        return total_active, max_streak

    # ── 评分计算 ──────────────────────────────────────────────────────────────

    def calculate_score(self) -> dict:
        """
        加权平衡评分，各维度贡献均衡。
        返回各分项和总分的字典。
        """
        total_cached = self.total_cached_input_tokens + self.total_cache_read_input_tokens
        total_active, max_streak = self.compute_streak()

        # 代码工具调用总次数
        code_tool_calls = sum(self.tool_counts[t] for t in CODE_TOOLS)
        # 高级工具种类数（去重）
        advanced_tool_types = sum(
            1 for t in self.tool_counts
            if t in ADVANCED_TOOLS or t.startswith("Agent:")
        )
        # 使用次数超过 5 次的 Skill 数量
        skills_over_5 = sum(1 for c in self.skill_counts.values() if c > 5)

        breakdown = {
            "消息量":    (self.total_messages // 500) * 0.2,
            "会话数":    (self.total_sessions // 30) * 0.3,
            "输入Token": (self.total_input_tokens // 5_000_000) * 0.3,
            "缓存Token": (total_cached // 5_000_000) * 0.15,
            "输出Token": (self.total_output_tokens // 50_000) * 0.1,
            "Skill深度": skills_over_5 * 0.4,
            "工具多样性": advanced_tool_types * 0.3,
            "代码操作量": (code_tool_calls // 200) * 0.2,
            "活跃天数":  total_active * 0.1,
        }
        breakdown["总分"] = sum(breakdown.values())
        breakdown["_skills_over_5"] = skills_over_5
        breakdown["_code_tool_calls"] = code_tool_calls
        breakdown["_advanced_tool_types"] = advanced_tool_types
        breakdown["_total_active"] = total_active
        breakdown["_max_streak"] = max_streak
        return breakdown

    # ── 报告输出 ──────────────────────────────────────────────────────────────

    def print_report(self):
        """输出完整统计报告"""
        now = datetime.now()
        one_month_ago = now - timedelta(days=30)
        total_cached = self.total_cached_input_tokens + self.total_cache_read_input_tokens
        sc = self.calculate_score()

        W = 70
        print("\n" + "═" * W)
        print(f"  Claude Code / Codex 使用统计  "
              f"({one_month_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})")
        print("═" * W)

        # ── 基础统计 ──
        print(f"  会话数:              {self.total_sessions:>10,}")
        print(f"  消息数:              {self.total_messages:>10,}")
        print(f"  活跃天数:            {sc['_total_active']:>10}  (最长连续 {sc['_max_streak']} 天)")
        print()

        # ── Token 统计 ──
        print(f"  输入 Token:          {self.total_input_tokens:>10,}")
        print(f"  缓存写入 Token:      {self.total_cached_input_tokens:>10,}")
        print(f"  缓存读取 Token:      {self.total_cache_read_input_tokens:>10,}")
        print(f"  缓存合计:            {total_cached:>10,}")
        print(f"  输出 Token:          {self.total_output_tokens:>10,}")
        print(f"  Token 总计:          {self.total_input_tokens + total_cached + self.total_output_tokens:>10,}")
        print()

        # ── 工具使用 ──
        print(f"  代码工具调用次数:    {sc['_code_tool_calls']:>10,}")
        print(f"  高级工具种类数:      {sc['_advanced_tool_types']:>10}")
        if self.tool_counts:
            top_tools = sorted(self.tool_counts.items(), key=lambda x: -x[1])[:8]
            print("  Top 工具调用:")
            for name, cnt in top_tools:
                print(f"    {name:<30} {cnt:>6,} 次")
        print()

        # ── Skill 统计 ──
        print(f"  不同 Skill 数:       {len(self.skill_counts):>10}")
        print(f"  Skill 总调用次数:    {self.total_skill_uses:>10,}")
        if self.skill_counts:
            print("  Top 10 Skill:")
            for i, (skill, cnt) in enumerate(
                sorted(self.skill_counts.items(), key=lambda x: -x[1])[:10], 1
            ):
                mark = "✓" if cnt > 5 else " "
                print(f"  {i:2d}. {skill:<36} {cnt:>5} 次 {mark}")
        print()

        # ── 得分明细 ──
        print("─" * W)
        print("  得分明细:")
        score_items = [
            ("消息量 (每 500 条 +0.2)",    "消息量"),
            ("会话数 (每 30 个 +0.3)",     "会话数"),
            ("输入 Token (每 500万 +0.3)", "输入Token"),
            ("缓存 Token (每 500万 +0.15)","缓存Token"),
            ("输出 Token (每 5万 +0.1)",   "输出Token"),
            ("Skill 深度 (>5次 每个 +0.4)","Skill深度"),
            ("工具多样性 (每种 +0.3)",     "工具多样性"),
            ("代码操作量 (每 200次 +0.2)", "代码操作量"),
            ("活跃天数 (每天 +0.1)",       "活跃天数"),
        ]
        for label, key in score_items:
            print(f"  {label:<36} {sc[key]:>7.2f}")
        print("─" * W)
        print(f"  {'总分':<36} {sc['总分']:>7.2f}")
        print("═" * W + "\n")


# ─── 主程序 ───────────────────────────────────────────────────────────────────

def main():
    cutoff_ts = (datetime.now() - timedelta(days=30)).timestamp()
    home = os.path.expanduser("~")
    collector = StatsCollector()

    # 扫描 Codex sessions
    codex_dir = os.path.join(home, '.codex', 'sessions')
    if os.path.exists(codex_dir):
        print("🔍 扫描 ~/.codex/sessions ...")
        for root, _, files in os.walk(codex_dir):
            for fn in files:
                if fn.endswith('.jsonl'):
                    collector.process_codex_session(os.path.join(root, fn), cutoff_ts)

    # 扫描 Claude Code 费用记录
    costs_file = os.path.join(home, '.claude', 'metrics', 'costs.jsonl')
    if os.path.exists(costs_file):
        print("🔍 扫描 ~/.claude/metrics/costs.jsonl ...")
        collector.process_costs_jsonl(costs_file, cutoff_ts)

    # 扫描 Claude Code 项目会话
    claude_dir = os.path.join(home, '.claude', 'projects')
    if os.path.exists(claude_dir):
        print("🔍 扫描 ~/.claude/projects ...")
        for root, _, files in os.walk(claude_dir):
            for fn in files:
                if fn.endswith('.jsonl'):
                    collector.process_claude_project_jsonl(os.path.join(root, fn), cutoff_ts)

    collector.print_report()


if __name__ == '__main__':
    main()

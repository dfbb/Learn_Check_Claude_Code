#!/usr/bin/env python3
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta


class StatsCollector:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_cached_input_tokens = 0
        self.total_cache_read_input_tokens = 0
        self.total_output_tokens = 0
        self.total_sessions = 0
        self.total_messages = 0
        self.total_skill_uses = 0
        self.skill_counts = defaultdict(int)

    def extract_tokens(self, obj):
        """从对象中提取各种 token 计数"""
        if 'input_tokens' in obj:
            self.total_input_tokens += obj['input_tokens']
        if 'cached_input_tokens' in obj:
            self.total_cached_input_tokens += obj['cached_input_tokens']
        if 'cache_read_input_tokens' in obj:
            self.total_cache_read_input_tokens += obj['cache_read_input_tokens']
        if 'output_tokens' in obj:
            self.total_output_tokens += obj['output_tokens']

    def process_codex_session(self, file_path, one_month_ago_ts):
        """处理 .codex/sessions 目录下的 jsonl 文件"""
        if not self.is_recent_file(file_path, one_month_ago_ts):
            return

        self.total_sessions += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # 检查时间戳
                    if 'timestamp' in data and not self.is_recent_timestamp(data['timestamp'], one_month_ago_ts):
                        continue

                    # 每一行算一条消息
                    self.total_messages += 1

                    # 统计 token 数量 - 多种格式兼容
                    processed = False

                    # 格式 1: Codex event_msg 类型的 token_count 事件
                    if data.get('type') == 'event_msg':
                        payload = data.get('payload', {})
                        if (isinstance(payload, dict) and
                            payload.get('type') == 'token_count' and 'info' in payload):
                            info = payload['info']
                            if isinstance(info, dict):
                                # Codex 格式优先使用 last_token_usage（本轮新增），避免累计重复
                                # 因为 total_token_usage 是累计总数，每步都会包含之前所有量
                                if 'last_token_usage' in info:
                                    usage = info['last_token_usage']
                                    self.extract_tokens(usage)
                                    processed = True
                                elif 'total_token_usage' in info:
                                    usage = info['total_token_usage']
                                    self.extract_tokens(usage)
                                    processed = True
                                elif 'input_tokens' in info:
                                    self.extract_tokens(info)
                                    processed = True

                    # 格式 2: Claude Code 直接有 usage 字段
                    if not processed and 'usage' in data:
                        usage = data['usage']
                        if isinstance(usage, dict):
                            self.extract_tokens(usage)
                            processed = True

                    # 格式 3: 顶级直接有 tokens 字段
                    if not processed:
                        self.extract_tokens(data)

                    # 统计 Skill 调用 - 直接检查 skill 字段
                    if 'skill' in data:
                        skill_name = data['skill']
                        if isinstance(skill_name, str) and skill_name:
                            self.skill_counts[skill_name] += 1
                            self.total_skill_uses += 1

        except Exception as e:
            # 跳过错误，许多文件可能有不完整的行
            pass

    def process_costs_jsonl(self, file_path, one_month_ago_ts):
        """处理 .claude/metrics/costs.jsonl 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if 'timestamp' in data and not self.is_recent_timestamp(data['timestamp'], one_month_ago_ts):
                        continue

                    self.extract_tokens(data)
                    self.total_messages += 1
        except Exception as e:
            print(f"处理 {file_path} 出错: {e}")

    def process_claude_project_jsonl(self, file_path, one_month_ago_ts):
        """处理 .claude/projects 目录下的 jsonl 文件"""
        if not self.is_recent_file(file_path, one_month_ago_ts):
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = True
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # 检查时间戳
                    if 'timestamp' in data and not self.is_recent_timestamp(data['timestamp'], one_month_ago_ts):
                        continue

                    # 每个文件算一个 session
                    if first_line:
                        self.total_sessions += 1
                        first_line = False

                    # 统计消息
                    if 'type' in data:
                        if data['type'] in ['user', 'assistant']:
                            self.total_messages += 1
                    elif 'message' in data or 'content' in data:
                        self.total_messages += 1

                    # 检查是否是新会话（另一种格式）
                    if 'type' in data and data['type'] == 'user' and data.get('parentUuid') is None:
                        self.total_sessions += 1

                    # 提取 token 使用量
                    if 'message' in data and isinstance(data['message'], dict) and 'usage' in data['message']:
                        usage = data['message']['usage']
                        self.extract_tokens(usage)
                    elif 'usage' in data:
                        usage = data['usage']
                        if isinstance(usage, dict):
                            self.extract_tokens(usage)

                    # 统计 Skill 调用
                    if ('message' in data and isinstance(data['message'], dict) and
                        'content' in data['message']):
                        content = data['message']['content']
                        if isinstance(content, list):
                            for item in content:
                                if item.get('type') == 'tool_use':
                                    name = item.get('name')
                                    if name == 'Skill':
                                        input_data = item.get('input', {})
                                        if 'skill' in input_data:
                                            skill_name = input_data['skill']
                                            self.skill_counts[skill_name] += 1
                                            self.total_skill_uses += 1
                                    elif name == 'Agent':
                                        input_data = item.get('input', {})
                                        if 'subagent_type' in input_data:
                                            agent_type = input_data['subagent_type']
                                            self.skill_counts[f"Agent:{agent_type}"] += 1
                                            self.total_skill_uses += 1

                    # 直接的 skill 调用格式
                    if 'skill' in data:
                        skill_name = data['skill']
                        if isinstance(skill_name, str) and skill_name:
                            self.skill_counts[skill_name] += 1
                            self.total_skill_uses += 1
                    elif 'name' in data and data['name'] == 'Skill' and 'input' in data:
                        input_data = data['input']
                        if 'skill' in input_data:
                            skill_name = input_data['skill']
                            self.skill_counts[skill_name] += 1
                            self.total_skill_uses += 1

        except Exception as e:
            # 跳过错误
            pass

    @staticmethod
    def is_recent_timestamp(timestamp_str, one_month_ago_ts):
        """检查时间戳是否在最近一个月内"""
        try:
            if isinstance(timestamp_str, str):
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                return dt.timestamp() >= one_month_ago_ts
            elif isinstance(timestamp_str, (int, float)):
                return timestamp_str >= one_month_ago_ts
        except:
            return False
        return False

    @staticmethod
    def is_recent_file(file_path, one_month_ago_ts):
        """检查文件是否在最近一个月内修改"""
        mtime = os.path.getmtime(file_path)
        return mtime >= one_month_ago_ts

    def calculate_score(self):
        """根据规则计算得分

        计分规则：
        - 每 1000 条消息 +0.3 分
        - 每 50 个 session +0.5 分
        - 每 1000万 input_token +0.5 分
        - 每 1000万 cached_input_tokens(cache_read_input_tokens) +0.2 分
        - 每 10万 output_token +0.1 分
        - 每个使用次数超过 5 次的 skill +0.5 分
        """
        score = 0.0
        score += (self.total_messages // 1000) * 0.3
        score += (self.total_sessions // 50) * 0.5
        score += (self.total_input_tokens // 10_000_000) * 0.5
        total_cached = self.total_cached_input_tokens + self.total_cache_read_input_tokens
        score += (total_cached // 10_000_000) * 0.2
        score += (self.total_output_tokens // 100_000) * 0.1

        skills_over_5 = sum(1 for cnt in self.skill_counts.values() if cnt > 5)
        score += skills_over_5 * 0.5

        return score, skills_over_5

    def print_report(self):
        """打印美观的统计报告"""
        one_month_ago = datetime.now() - timedelta(days=30)
        score, skills_over_5 = self.calculate_score()
        total_cached = self.total_cached_input_tokens + self.total_cache_read_input_tokens

        print("\n" + "═" * 70)
        print(f"📊 最近 30 天使用统计 ({one_month_ago.strftime('%Y-%m-%d')} 至 {datetime.now().strftime('%Y-%m-%d')})")
        print("═" * 70)
        print(f"🔹 总会话数:          {self.total_sessions:,}")
        print(f"🔹 总消息数:          {self.total_messages:,}")
        print(f"🔹 输入 Token 总数:   {self.total_input_tokens:,}")
        print(f"🔹 cached_input_tokens:  {self.total_cached_input_tokens:,}")
        print(f"🔹 cache_read_input_tokens: {self.total_cache_read_input_tokens:,}")
        print(f"🔹 缓存总计:          {total_cached:,}")
        print(f"🔹 输出 Token 总数:   {self.total_output_tokens:,}")
        print(f"🔹 Token 合计:        {self.total_input_tokens + total_cached + self.total_output_tokens:,}")
        print(f"🔹 使用过的不同 Skill: {len(self.skill_counts)} 个")
        print(f"🔹 Skill 总调用次数:   {self.total_skill_uses} 次")
        print()

        print("📈 使用频次 Top 10 Skill:")
        print("─" * 60)
        sorted_skills = sorted(self.skill_counts.items(), key=lambda x: -x[1])
        for i, (skill, count) in enumerate(sorted_skills[:10], 1):
            mark = "✓" if count > 5 else " "
            print(f"{i:2d}. {skill:<36} {count:>5} 次 {mark}")
        print()

        print("🧮 得分计算:")
        print("─" * 60)
        print(f"{'消息数 (每 1000 条 +0.3)':<35} {(self.total_messages // 1000) * 0.3:>8.2f}")
        print(f"{'会话数 (每 50 个 +0.5)':<35} {(self.total_sessions // 50) * 0.5:>8.2f}")
        print(f"{'输入 Token (每 1000万 +0.5)':<35} {(self.total_input_tokens // 10_000_000) * 0.5:>8.2f}")
        print(f"{'缓存总计 (每 1000万 +0.2)':<35} {(total_cached // 10_000_000) * 0.2:>8.2f}")
        print(f"{'输出 Token (每 10万 +0.1)':<35} {(self.total_output_tokens // 100_000) * 0.1:>8.2f}")
        print(f"{'Skill (使用>5次 每个 +0.5)':<35} {skills_over_5 * 0.5:>8.2f}  ({skills_over_5} 个)")
        print("─" * 60)
        print(f"{'🏆 最终总分':<35} {score:>8.2f}")
        print("─" * 60)


def main():
    # 计算一个月前的日期
    one_month_ago = datetime.now() - timedelta(days=30)
    one_month_ago_ts = one_month_ago.timestamp()

    collector = StatsCollector()

    # 开始扫描
    home = os.path.expanduser("~")
    print("🔍 正在扫描 .codex/sessions...")
    codex_dir = os.path.join(home, '.codex/sessions')
    if os.path.exists(codex_dir):
        for root, dirs, files in os.walk(codex_dir):
            for filename in files:
                if filename.endswith('.jsonl'):
                    file_path = os.path.join(root, filename)
                    collector.process_codex_session(file_path, one_month_ago_ts)

    print("🔍 正在扫描 .claude/metrics...")
    costs_file = os.path.join(home, '.claude/metrics/costs.jsonl')
    if os.path.exists(costs_file):
        collector.process_costs_jsonl(costs_file, one_month_ago_ts)

    print("🔍 正在扫描 .claude/projects...")
    claude_dir = os.path.join(home, '.claude/projects')
    if os.path.exists(claude_dir):
        for root, dirs, files in os.walk(claude_dir):
            for filename in files:
                if filename.endswith('.jsonl'):
                    file_path = os.path.join(root, filename)
                    collector.process_claude_project_jsonl(file_path, one_month_ago_ts)

    # 输出报告
    collector.print_report()


if __name__ == '__main__':
    main()

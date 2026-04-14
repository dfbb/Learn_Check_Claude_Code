# Claude Check

Claude Code 使用情况检测与学习工具集。

---

## scripts/check-programmer-code-cli.py

统计过去 30 天内 Claude Code / Codex 的使用数据，并计算一个综合得分。

**扫描来源：**
- `~/.codex/sessions/` — Codex 会话 JSONL
- `~/.claude/metrics/costs.jsonl` — Claude Code 费用记录
- `~/.claude/projects/` — Claude Code 项目会话 JSONL

**输出内容：**
- 会话数、消息数、各类 Token 用量
- Top 10 Skill 调用频次
- 综合得分（基于消息量、Token 量、Skill 使用深度）

**计分规则：**

| 指标 | 得分 |
|------|------|
| 每 1000 条消息 | +0.3 |
| 每 50 个 session | +0.5 |
| 每 1000 万 input token | +0.5 |
| 每 1000 万缓存 token | +0.2 |
| 每 10 万 output token | +0.1 |
| 每个使用超过 5 次的 Skill | +0.5 |

**使用方法：**

```bash
python3 scripts/check-programmer-code-cli.py
```

---

## quiz/

Claude Code 知识测验 Web 应用（Go 实现）。

**题库：** `quiz/questions-zh/` 下 16 个分类，涵盖快速入门、核心概念、Memory、Agents、Skills、Hooks、MCP、安全、架构等主题。

**难度级别：**
- `junior`（初级）— 20 题
- `senior`（中级）— 30 题
- `power`（高级）— 30 题

**使用方法：**

```bash
cd quiz

# 方式一：直接运行预编译二进制
./quiz-server

# 方式二：从源码运行
go run main.go
```

启动后访问 http://localhost:8080，输入姓名、选择难度开始答题。

答题结果自动追加写入 `result.txt`，包含每题对错、用时和得分百分比。

---

## docs/

Claude Code 参考文档：

| 文件 | 说明 |
|------|------|
| `ClaudeCode_CheatSheet.md` | Claude Code 常用命令速查表 |
| `ClaudeCode_Ultimate_Guide.zh-CN.md` | Claude Code 完整中文使用指南 |
| `ClaudeCode_BestPractise.md` | Claude Code 最佳实践 |

---

## 鸣谢

- 题库内容参考自 [FlorianBruniaux/claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/quiz)
- 评分脚本灵感来自知乎用户 [Alex Hu](https://zhuanlan.zhihu.com/p/2009744974980331332)

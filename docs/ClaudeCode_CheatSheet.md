

# Claude Code 速查表



---

## 核心命令

| 命令                 | 作用                                              |
| ------------------ | ----------------------------------------------- |
| `/help`            | 上下文帮助                                           |
| `/powerup`         | 交互式动画教程，教你使用 Claude Code 的各种功能                  |
| `/clear`           | 重置对话                                            |
| `/compact`         | 释放上下文空间                                         |
| `/status`          | 会话状态 + 上下文用量                                    |
| `/context`         | 详细的 Token 用量明细                                  |
| `/plan`            | 进入计划模式（不做任何修改）                                  |
| `/ultraplan`       | 云端计划模式 — 在云端起草、浏览器中审阅（v2.1.91+）                 |
| `/execute`         | 退出计划模式（应用更改）                                    |
| `/model`           | 切换模型（sonnet/opus/opusplan）                      |
| `/effort [级别]`     | 设置推理强度：`low`、`medium`、`high`（持久化到 settings）     |
| `/insights`        | 使用分析 + 优化报告                                     |
| `/simplify`        | 检测已更改代码中的过度设计并自动修复                              |
| `/batch`           | 通过 5–30 个并行工作树智能体进行大规模重构                        |
| `/teleport`        | 从网页端传送会话到本地                                     |
| `/desktop`         | 将终端会话移交给桌面应用（可视化 diff 审阅）                       |
| `/schedule`        | 创建云端定时任务                                        |
| `/tasks`           | 监控后台任务                                          |
| `/remote-env`      | 配置云端环境                                          |
| `/remote-control`  | 启动远程控制会话（研究预览版，Pro/Max 可用）                      |
| `/rc`              | `/remote-control` 的简写                           |
| `/mobile`          | 获取 Claude 移动应用下载链接                              |
| `/fast`            | 切换快速模式（速度提升 2.5 倍，成本增加 6 倍）                     |
| `/voice`           | 切换语音输入（按住空格说话，松开发送）                             |
| `/btw [问题]`        | 侧边快速提问 — 只读临时智能体，不污染历史记录，不使用工具                  |
| `/loop [间隔] [提示词]` | 循环运行提示词（例：`/loop 5m check the deploy`，默认 10 分钟） |
| `/stats`           | 使用图表、常用模型、连续使用天数                                |
| `/rename [名称]`     | 命名或重命名当前会话                                      |
| `/copy`            | 交互式选择器，复制代码块或完整回复                               |
| `/debug`           | 系统化故障排查                                         |
| `/config`          | 打开设置界面（标签式，可修改所有配置）                             |
| `/exit`            | 退出（或按 Ctrl+D）                                   |

---

## 键盘快捷键

| 快捷键           | 作用                  |
| ------------- | ------------------- |
| `Shift+Tab`   | 循环切换权限模式            |
| `Esc` × 2     | 回退（撤销）              |
| `Ctrl+C`      | 中断                  |
| `Ctrl+R`      | 搜索命令历史              |
| `Ctrl+L`      | 清屏（保留上下文）           |
| `Tab`         | 自动补全                |
| `Shift+Enter` | 换行                  |
| `Ctrl+B`      | 后台任务                |
| `Ctrl+F`      | 终止所有后台智能体（连按两次）     |
| `Alt+T`       | 开关思考模式              |
| `Space`（按住）   | 语音输入（需先开启 `/voice`） |
| `Ctrl+D`      | 退出                  |

---

## 文件引用

```
@path/to/file.ts    → 引用文件
@agent-name         → 调用智能体
!shell-command      → 运行 shell 命令
```

| IDE       | 快捷键            |
| --------- | -------------- |
| VS Code   | `Alt+K`        |
| JetBrains | `Cmd+Option+K` |

---

## 安装方式

```bash
# macOS/Linux/WSL（推荐，自动更新）
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell（自动更新）
irm https://claude.ai/install.ps1 | iex

# Homebrew（不自动更新，需手动 brew upgrade claude-code）
brew install --cask claude-code
# stable 频道（约延迟一周，跳过重大回归版本）：
brew install --cask claude-code@latest

# WinGet（不自动更新）
winget install Anthropic.ClaudeCode
```

---

## 鲜为人知但官方支持的功能

| 功能          | 推出时间       | 说明                                                                                                                           |
| ----------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **任务 API**      | v2.1.16    | 支持依赖关系的持久化任务列表                                                                                                               |
| **后台智能体**       | v2.0.60    | 子智能体在你编码时并行工作                                                                                                                |
| **智能体团队**       | v2.1.32    | 多智能体协调（TeamCreate/SendMessage）                                                                                               |
| **自动记忆**        | v2.1.32    | 自动跨会话捕获上下文                                                                                                                   |
| **会话分叉**        | v2.1.19    | 回退 + 创建平行时间线（`--fork-session`）                                                                                               |
| **LSP 工具**      | v2.0.74    | 类 IDE 导航：符号、类型、引用。约 50 毫秒，而用 grep 可能要 45 秒。支持 11 种语言                                                                         |
| **语音模式**        | v2.1.x     | 原生语音输入，免费转录，不影响速率限制                                                                                                          |
| **远程控制**        | v2.1.51    | 从手机/浏览器控制本地会话（研究预览版，Pro/Max 可用）                                                                                              |
| **`/loop`**     | v2.1.71    | 会话级循环调度器：`/loop 5m check the deploy`（会话结束即停止）。最小 1 分钟，每会话最多 50 个任务                                                           |
| **云端定时任务**      | 2026       | 通过 `/schedule` 或 `claude.ai/code/scheduled` 实现关机后仍运行的调度。在 Anthropic 基础设施上运行，每次执行都重新克隆仓库，最小间隔 1 小时。Pro/Max/Team/Enterprise 可用 |
| **桌面定时任务**      | 2026       | 通过桌面应用实现本地机器调度。最小 1 分钟，完全访问本地文件，无需保持会话                                                                                       |
| **技能评估**        | 2026 年 3 月 | 两种技能类型：能力提升（填补模型短板，会衰减）/ 偏好编码（固化工作流程，持续生效）。支持基准模式、A/B 测试、触发调优。                                                               |
| **输出样式**        | 2025 年 8 月 | `/config` → "首选输出样式"：**默认**（简洁）、**解释型**（增加设计原理说明）、**学习型**（结对编程风格，带 `TODO(human)` 标记）。可通过 `.claude/styles/` 自定义样式。            |
| **Git 工作树**     | 2026       | `claude -w <名称>` 在隔离分支并行工作；`--tmux` 自动创建 tmux 窗格                                                                             |
| **Chrome 集成**   | 2026       | `claude --chrome` 调试实时 Web 应用，浏览器自动化测试                                                                                       |
| **Channels**    | 2026（研究预览） | 接收 Telegram/Discord/iMessage/Webhook 推送，触发 Claude 会话                                                                         |
| **Slack 集成**    | 2026       | 在 Slack 中 @Claude，从 bug 报告自动生成 PR                                                                                            |
| **Agent SDK**   | 2026       | 构建自定义智能体，完全控制编排/工具/权限/结构化输出                                                                                                  |
| **Bare 模式**     | 2026       | `--bare` 跳过所有自动发现（钩子/插件/MCP/记忆），脚本调用启动更快                                                                                     |
| **`--remote`**  | 2026       | `claude --remote "任务"` 直接在 claude.ai 创建云端会话                                                                                  |
| **`/desktop`**  | 2026       | 将终端会话移交桌面应用进行可视化 diff 审阅                                                                                                      |
| **Dispatch**    | 2026       | 从手机发送任务给桌面应用，桌面自动创建并执行会话                                                                                                      |

**激活 LSP**：在 `~/.claude/settings.json` 中添加 `{ "env": { "ENABLE_LSP_TOOL": "1" } }`（需为对应语言安装 LSP 服务器：`tsserver`、`pylsp`、`gopls`、`rust-analyzer`、`sourcekit-lsp` 等）

**专业提示**：这些不是"秘密"——它们都写在 [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) 里。去读一读！

---

## 权限模式

| 模式                | 编辑      | 执行          | 说明                              |
| ----------------- | ------- | ----------- | ------------------------------- |
| Default           | 询问      | 询问          | 标准模式                            |
| acceptEdits       | 自动      | 询问          | 自动接受文件编辑                        |
| Plan Mode         | ❌       | ❌           | 只读探索，不做任何修改                     |
| auto              | 智能判断    | 智能判断        | AI 分类器自动决策（Team/Enterprise/API） |
| dontAsk           | 仅在允许规则内 | 仅在允许规则内     | 严格按规则执行                         |
| bypassPermissions | 自动      | 自动（仅 CI/CD） | 跳过所有确认                          |

**按 `Shift+Tab` 切换模式**

- `--enable-auto-mode`：将 auto 模式加入 Shift+Tab 循环（需 Team/Enterprise/API + Sonnet 4.6 或 Opus 4.6）
- `--allow-dangerously-skip-permissions`：将 bypassPermissions 加入循环但不以它启动

---

## 记忆与设置（四级作用域）

| 作用域        | 位置                                          | 影响范围       | 团队共享 |
| ---------- | ------------------------------------------- | ---------- | ---- |
| **Managed** | MDM/注册表/`managed-settings.json`            | 机器上所有用户    | ✅ IT 部署 |
| **User**   | `~/.claude/settings.json`                   | 你（所有项目）    | ❌    |
| **Project** | `.claude/settings.json`                     | 所有协作者      | ✅ 提交到 git |
| **Local**  | `.claude/settings.local.json`               | 你（此项目）     | ❌ gitignored |

**优先级**：Managed > 命令行参数 > Local > Project > User

| 文件                    | 位置                                          | 用途            |
| --------------------- | ------------------------------------------- | ------------- |
| `CLAUDE.md`           | 项目根目录 或 `.claude/CLAUDE.md`                 | 团队记忆（指令）      |
| `CLAUDE.local.md`     | 项目根目录                                       | 个人覆盖（不提交）     |
| `settings.json`       | `.claude/`                                  | 团队设置（钩子/权限）   |
| `settings.local.json` | `.claude/`                                  | 你的个人设置覆盖      |
| `CLAUDE.md`           | `~/.claude/`                                | 个人全局记忆        |
| `.mcp.json`           | 项目根目录                                       | 项目级 MCP 服务器   |
| `~/.claude.json`      | 用户主目录                                       | 偏好/OAuth/MCP缓存 |

### 常用 settings.json 选项

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny": ["Bash(curl *)", "Read(./.env)"]
  },
  "effortLevel": "medium",
  "language": "chinese",
  "autoUpdatesChannel": "stable",
  "alwaysThinkingEnabled": false,
  "env": { "CLAUDE_CODE_ENABLE_TELEMETRY": "1" },
  "hooks": { "PostToolUse": [{ "matcher": "Edit", "hooks": [{ "type": "command", "command": "npm run lint" }] }] }
}
```

| 设置键                    | 说明                                          |
| ---------------------- | ------------------------------------------- |
| `effortLevel`          | 持久化推理强度：`low`/`medium`/`high`               |
| `language`             | Claude 回复语言（如 `"chinese"`、`"japanese"`）     |
| `autoUpdatesChannel`   | 更新频道：`"latest"`（默认）或 `"stable"`（约延迟一周）      |
| `alwaysThinkingEnabled` | 默认开启扩展思考                                   |
| `defaultMode`          | 默认权限模式                                      |
| `autoMemoryDirectory`  | 自定义自动记忆存储目录                                 |
| `disableAllHooks`      | 禁用所有钩子和状态栏                                  |
| `includeGitInstructions` | 是否在系统提示中包含 git 工作流指令（默认 `true`）           |
| `attribution`          | 自定义 git 提交/PR 的署名（替代旧版 `includeCoAuthoredBy`） |
| `fastModePerSessionOptIn` | `true` = 快速模式不跨会话持久化，每次需手动 `/fast` 开启    |
| `availableModels`      | 限制用户可选模型列表                                  |
| `companyAnnouncements` | 启动时显示的公告（企业用）                               |

---

## `.claude/` 文件夹结构

```
.claude/
├── CLAUDE.md           # 本地记忆（gitignored）
├── settings.json       # 钩子（提交到仓库）
├── settings.local.json # 权限设置（不提交）
├── agents/             # 自定义智能体
├── commands/           # 斜杠命令
├── hooks/              # 事件脚本
├── rules/              # 自动加载的规则
├── skills/             # 知识模块
└── worktrees/          # git 工作树（claude -w 创建）
```

---

## 平台与集成（新）

| 平台/集成              | 用途                                    | 入口                                  |
| ------------------ | ------------------------------------- | ----------------------------------- |
| **Web**            | 浏览器中运行，无需本地安装，支持长任务                   | `claude.ai/code`                    |
| **Desktop App**    | 独立桌面应用，可视化 diff，多会话并排，调度任务            | 下载 macOS/Windows 安装包                |
| **VS Code**        | 内联 diff、@提及、计划审阅、会话历史                 | 扩展市场搜索 "Claude Code"                |
| **JetBrains**      | 交互式 diff、选择上下文共享                      | JetBrains Marketplace               |
| **Chrome**         | 调试实时 Web 应用，浏览器自动化                    | `claude --chrome`                   |
| **GitHub Actions** | 自动化 PR 审阅、Issue 分类                    | 参见 GitHub Actions 文档                |
| **GitLab CI/CD**   | GitLab 流水线集成                          | 参见 GitLab CI/CD 文档                  |
| **GitHub Code Review** | 每个 PR 自动代码审阅                      | 参见 Code Review 文档                   |
| **Slack**          | 在 Slack 中 @Claude，从 bug 报告生成 PR      | 参见 Slack 集成文档                       |
| **Channels**       | 接收 Telegram/Discord/iMessage/Webhook 推送 | `--channels plugin:<name>@<marketplace>` |
| **Agent SDK**      | 构建自定义智能体，完全控制编排/工具/权限                | 参见 Agent SDK 文档                     |

---

## Git 工作树（并行会话）

```bash
# 在隔离工作树中启动（自动命名）
claude -w feature-auth

# 配合 tmux（iTerm2 原生窗格）
claude -w feature-auth --tmux

# 传统 tmux
claude -w feature-auth --tmux=classic

# 恢复关联到 PR 的会话
claude --from-pr 123
```

**用途**：同时在多个功能分支上并行工作，互不干扰。

---

## 典型工作流程

```
1. 启动会话      → claude
2. 检查上下文      → /status
3. 计划模式          → Shift+Tab × 2（复杂任务时使用）
4. 描述任务      → 清晰、具体的提示词
5. 审阅更改     → 务必阅读 diff（差异对比）！
6. 接受/拒绝      → 输入 y/n 确认
7. 验证             → 运行测试
8. 提交             → 任务完成后
9. /compact           → 上下文超过 70% 时
```

---

## 上下文管理（关键）

### 状态栏

```
Model: Sonnet | Ctx: 89.5k | Cost: $2.11 | Ctx(u): 56.0%
```

**关注 `Ctx(u)`：** → >70% = `/compact`，>85% = `/clear`

**增强状态栏 ([ccstatusline](https://github.com/sirmalloc/ccstatusline))：** 添加到 `~/.claude/settings.json`：

```json
{ "statusLine": { "type": "command", "command": "npx -y ccstatusline@latest", "padding": 0 } }
```

### 上下文阈值

| 上下文占比  | 状态  | 操作            |
| ------ | --- | ------------- |
| 0-50%  | 绿色  | 自由工作          |
| 50-70% | 黄色  | 有选择地使用        |
| 70-90% | 橙色  | 立即 `/compact` |
| 90%+   | 红色  | 必须 `/clear`   |

### 根据表现处理

| 迹象       | 操作         |
| -------- | ---------- |
| 回复变短     | `/compact` |
| 频繁遗忘     | `/clear`   |
| 上下文 >70% | `/compact` |
| 任务完成     | `/clear`   |

### 上下文恢复命令

| 命令               | 用途             |
| ---------------- | -------------- |
| `/compact`       | 总结并释放上下文       |
| `/clear`         | 重新开始           |
| `/rewind`        | 撤销最近更改         |
| `claude -c`      | 恢复上次会话（CLI 参数） |
| `claude -r <id>` | 恢复指定会话（CLI 参数） |

---

## 内部机制（快速概览）

| 概念       | 要点                                                  |
| -------- | --------------------------------------------------- |
| **主循环**  | 简单的 `while(tool_call)` — 没有 DAG，没有分类器               |
| **工具**   | 8 个核心：Bash、Read、Edit、Write、Grep、Glob、Task、TodoWrite |
| **上下文**  | 约 200K token，在 75-92% 时自动压缩                         |
| **子智能体** | 隔离上下文，最大深度 = 1                                      |
| **理念**   | "更少脚手架，更多依靠模型本身" — 信任 Claude 的推理能力                  |

**深度解析**：[架构与内部机制](./core/architecture.md)

---

## 计划模式与思考

| 功能            | 激活方式                      | 用途                                    |
| ------------- | ------------------------- | ------------------------------------- |
| **计划模式**      | `Shift+Tab × 2` 或 `/plan` | 探索而不修改                                |
| **OpusPlan**  | `/model opusplan`         | Opus 负责计划，Sonnet 负责执行                 |
| **Ultraplan** | `/ultraplan <提示词>`        | 云端计划，浏览器审阅，终端保持空闲（v2.1.91+，需要 GitHub） |

> **Opus 4.6**（v2.1.68+）：Max/Team 用户默认推理强度为 **medium**。使用 `ultrathink` 可强制下一回合使用高强度推理。"think hard" 没有实际作用。

| 控制                                          | 操作                                    | 持久性      |
| ------------------------------------------- | ------------------------------------- | -------- |
| **Alt+T**                                   | 开关思考模式                                | 会话级      |
| **/config**                                 | 全局启用/禁用                               | 永久       |
| **`/model` 滑块**                             | 左右箭头：`low\|medium\|high`              | 会话级      |
| **`CLAUDE_CODE_EFFORT_LEVEL`**              | 环境变量：`low\|medium\|high`              | Shell 会话 |
| **`effortLevel` 设置**                        | 在 settings.json 中：`low\|medium\|high` | 永久       |
| **skill frontmatter 中的 `effort`**（v2.1.80+） | 每次调用覆盖：`low\|medium\|high`            | 每次调用     |

**成本提示**：简单任务时，按 Alt+T 关闭思考模式 → 更快更省。

**按技能设置推理强度** — 为机械性技能（commit、sync、scaffold）添加 `effort: low`，为分析性技能（security-audit、architecture-review）添加 `effort: high`。自动覆盖会话设置。

**OpusPlan 工作流程**：`/model opusplan` → `Shift+Tab × 2`（用 Opus 计划） → `Shift+Tab`（用 Sonnet 执行）

**Ultraplan 工作流程**：`/ultraplan <任务>` → 终端保持空闲，云端起草 → 浏览器中内联审阅 → 批准 → 在网页上执行（PR）或传送回终端

**适用于**：涉及 3 个以上文件的功能、架构设计、复杂调试

### 快速模型选择

| 任务            | 模型     | 推理强度        |
| ------------- | ------ | ----------- |
| 重命名、样板代码、测试生成 | Haiku  | low         |
| 功能开发、调试、重构    | Sonnet | medium–high |
| 架构设计、安全审计     | Opus   | high–max    |

> 完整决策表与成本估算：[第 2.5 节 模型选择与思考指南](ultimate-guide.md#25-model-selection--thinking-guide)

### 动态模型切换（会话中切换）

**模式**：以 Sonnet 启动（速度）→ 换到 Opus（复杂任务）→ 回到 Sonnet

**工作流程**：

```bash
# 会话开始（默认 Sonnet）
claude

# 遇到复杂功能
> "用 PKCE 实现 OAuth2 流程"
/model opus                    # 切换到深度推理

# 功能完成，回到日常任务
/model sonnet                  # 速度 + 成本优化
```

**最佳实践**：

- ✅ 在**任务边界**处切换，不要任务中途切换
- ✅ 用 Opus 处理：架构决策、复杂调试、安全关键代码
- ✅ 用 Sonnet 处理：日常编辑、重构、测试编写
- ✅ 用 Haiku 处理：简单修复、拼写错误、验证检查
- ❌ 不要在实现中途切换（会丢失上下文）

**成本影响**：
| 模型 | 输入 | 输出 | 使用场景 |
|-------|--------|--------|----------|
| Opus  | $15/MTok | $75/MTok | 复杂推理（10-20% 的任务） |
| Sonnet | $3/MTok | $15/MTok | 大部分开发工作（70-80% 的任务） |
| Haiku | $0.25/MTok | $1.25/MTok | 简单验证（5-10% 的任务） |

**动态切换**在保持复杂任务质量的同时优化了成本。

**来源**：[Gur Sannikov 嵌入式工程工作流程](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

## MCP 服务器

| 服务器            | 用途                 |
| -------------- | ------------------ |
| **Serena**     | 索引 + 会话记忆 + 符号搜索   |
| **grepai**     | 语义搜索 + 调用图分析       |
| **Context7**   | 库文档查询              |
| **Sequential** | 结构化推理              |
| **Playwright** | 浏览器自动化             |
| **Postgres**   | 数据库查询              |
| **doobidoo**   | 语义记忆 + 多客户端 + 知识图谱 |

**Serena 记忆**：`write_memory()` / `read_memory()` / `list_memories()`

**Serena 索引构建**：

```bash
# 初始索引
uvx --from git+https://github.com/oraios/serena serena project index

# 强制重建
serena project index --force-full

# 增量更新（更快）
serena project index --incremental --parallel 4
```

检查状态：`/mcp`

---

## 创建自定义组件

### 智能体（`.claude/agents/my-agent.md`）

```yaml
---
name: my-agent
description: Use when [trigger]
model: sonnet
tools: Read, Write, Edit, Bash
---
# Instructions here
```

### 命令（`.claude/commands/my-command.md`）

```markdown
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
---
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

### 钩子（macOS/Linux: `.sh` | Windows: `.ps1`）

**Bash**（macOS/Linux）：

```bash
#!/bin/bash
INPUT=$(cat)
# Process JSON input
exit 0  # 0=continue, 2=block
```

**PowerShell**（Windows）：

```powershell
$input = [Console]::In.ReadToEnd() | ConvertFrom-Json
# Process JSON input
exit 0  # 0=continue, 2=block
```

---

## 反模式

| ❌ 不要   | ✅ 要                  |
| ------ | -------------------- |
| 模糊的提示词 | 用 @引用 指定文件 + 行号      |
| 不阅读就接受 | 阅读每一个 diff           |
| 忽略警告   | 在 70% 时使用 `/compact` |
| 跳过权限确认 | 永远不要在生产环境中这样做        |
| 只有负面约束 | 提供替代方案               |

---

## 快速提示词公式

```
WHAT: [具体的交付物]
WHERE: [文件路径]
HOW: [约束条件、方法]
VERIFY: [成功标准]
```

**示例：**

```
为登录表单添加输入验证。
WHERE: src/components/LoginForm.tsx
HOW: 使用 Zod schema，显示内联错误
VERIFY: 空邮箱显示错误，无效格式显示错误
```

---

## CLI 命令

| 命令                        | 用途                                    |
| ------------------------- | ------------------------------------- |
| `claude`                  | 启动交互会话                                |
| `claude "query"`          | 带初始提示词启动                              |
| `claude -p "query"`       | 非交互模式（CI/CD），执行后退出                    |
| `claude -c`               | 继续当前目录最近的会话                           |
| `claude -r "<名称或ID>"`     | 恢复指定会话                                |
| `claude update`           | 更新到最新版本                               |
| `claude auth login`       | 登录（`--console` 用 API 计费，`--sso` 强制SSO） |
| `claude auth logout`      | 登出                                    |
| `claude auth status`      | 查看认证状态（`--text` 人类可读格式）               |
| `claude agents`           | 列出所有已配置的子智能体                          |
| `claude auto-mode defaults` | 打印内置 auto 模式分类规则（JSON）              |
| `claude mcp`              | 管理 MCP 服务器                            |
| `claude plugin`           | 管理插件（别名：`claude plugins`）             |
| `claude remote-control`   | 以服务器模式启动远程控制（无本地交互会话）                 |
| `claude setup-token`      | 生成长效 OAuth token（用于 CI/脚本）            |

## CLI 参数快速参考

| 参数                                    | 用途                              |
| ------------------------------------- | ------------------------------- |
| `-p "query"`                          | 非交互模式（CI/CD）                    |
| `-c` / `--continue`                   | 继续上次会话                          |
| `-r` / `--resume <id或名称>`             | 恢复指定会话                          |
| `-n` / `--name <名称>`                  | 为会话设置显示名称                       |
| `--teleport`                          | 从网页端传送会话到本地                     |
| `--remote "任务描述"`                     | 在 claude.ai 创建新的云端会话            |
| `--remote-control` / `--rc`           | 启动支持远程控制的交互会话                   |
| `--model sonnet`                      | 更改模型                            |
| `--effort low\|medium\|high\|max`     | 设置推理强度（会话级，不持久化）                |
| `--add-dir ../lib`                    | 允许访问当前目录外的路径                    |
| `--permission-mode plan`              | 指定权限模式（default/acceptEdits/plan/auto/dontAsk/bypassPermissions） |
| `--enable-auto-mode`                  | 将 auto 模式加入 Shift+Tab 循环        |
| `--tools "Bash,Edit,Read"`            | 限制可用工具                          |
| `--allowedTools "Bash(git log *)"`    | 白名单工具（无需确认）                     |
| `--disallowedTools "Edit"`            | 黑名单工具（完全禁用）                     |
| `--max-budget-usd 5.00`              | 最大 API 支出限制（打印模式）               |
| `--max-turns 3`                       | 限制智能体轮次（打印模式）                   |
| `--system-prompt "..."`              | 替换整个系统提示词                       |
| `--append-system-prompt "..."`       | 追加到默认系统提示词                      |
| `--append-system-prompt-file ./f.txt` | 从文件追加系统提示词                      |
| `-w` / `--worktree [名称]`             | 在隔离的 git 工作树中运行                 |
| `--tmux`                              | 为工作树创建 tmux 会话（需配合 `-w`）        |
| `--fork-session`                      | 恢复时创建新会话 ID（配合 `-r` 或 `-c`）     |
| `--from-pr <PR号或URL>`                | 恢复关联到指定 GitHub PR 的会话           |
| `--chrome`                            | 启用 Chrome 浏览器集成                  |
| `--bare`                              | 极简模式：跳过钩子/插件/MCP/记忆自动发现，启动更快    |
| `--mcp-config ./mcp.json`            | 从文件加载 MCP 服务器                   |
| `--strict-mcp-config`                 | 仅使用 `--mcp-config` 中的 MCP，忽略其他  |
| `--json-schema '{...}'`              | 获取符合 JSON Schema 的结构化输出（打印模式）   |
| `--fallback-model sonnet`            | 主模型过载时自动回退（打印模式）                |
| `--dangerously-skip-permissions`     | 自动接受（谨慎使用）                      |
| `--debug "api,mcp"`                  | 调试输出（支持分类过滤）                    |
| `--debug-file /tmp/log`              | 将调试日志写入文件                       |
| `--verbose`                           | 详细日志，显示完整轮次输出                   |
| `--output-format json`               | 输出格式：`text`/`json`/`stream-json` |
| `--exclude-dynamic-system-prompt-sections` | 将机器相关内容移到首条用户消息（提升缓存命中率）  |

> 完整 CLI 参考：[code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)

---

## 调试命令

```bash
claude --version              # 版本
claude update                 # 检查/安装更新
claude doctor                 # 诊断
claude --debug "api,mcp"      # 详细模式（支持分类过滤）
claude --debug-file /tmp/log  # 调试日志写入文件
claude --verbose              # 显示完整轮次输出
claude --mcp-debug            # 调试 MCP
claude auth status --text     # 查看认证状态
/mcp                          # MCP 状态（Claude 内部）
```

---

## CI/CD 模式（无交互模式）

```bash
# 非交互执行
claude -p "analyze this file" src/api.ts

# JSON 输出
claude -p "review" --output-format json

# 流式 JSON 输出
claude -p "review" --output-format stream-json

# 结构化输出（JSON Schema 验证）
claude -p --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}' "review"

# 经济型模型
claude -p "lint" --model haiku

# 限制轮次
claude -p "fix typos" --max-turns 5

# 限制预算
claude -p "refactor" --max-budget-usd 2.00

# 主模型过载时回退
claude -p --fallback-model sonnet "query"

# 自动接受
claude -p "fix typos" --dangerously-skip-permissions

# 极简模式（跳过所有自动发现，启动更快）
claude --bare -p "query"

# 提升缓存命中率（多用户/多机器场景）
claude -p --exclude-dynamic-system-prompt-sections "query"

# 管道输入
tail -200 app.log | claude -p "有没有异常？"
git diff main --name-only | claude -p "检查这些文件的安全问题"
```

---

## 远程控制 — 移动端访问（v2.1.51+，研究预览版）

> **仅 Pro/Max 可用** — Team、Enterprise 或 API 密钥不可用

```bash
# 从终端启动（新会话）
claude remote-control

# 或在活跃会话内部：
/rc        #（或 /remote-control）
```

**从手机/平板/浏览器连接：**

1. 扫描 **QR 码**（启动后按空格键）
2. 或在浏览器 / Claude 移动应用中打开 **会话 URL**
3. 或：输入 `/mobile` → 显示 App Store + Play Store 链接

| ⚠️ 已知限制   | 详情                                      |
| --------- | --------------------------------------- |
| 1 个会话同时连接 | 仅允许一个远程会话处于活跃状态                         |
| 斜杠命令失效    | `/new`、`/compact` 远程使用时变成纯文本 → 请从本地终端使用 |
| 终端必须保持开启  | 关闭本地终端会结束会话                             |
| 网络超时      | 约 10 分钟断连 → 会话过期                        |

**高级：tmux 多会话**（绕过单会话限制）

```bash
tmux new-session -s dev
# 每个窗格 = 独立的 claude 会话
# 在你想远程控制的窗格中运行 /rc
```

**自动启用：** `/config` → 切换 "Remote Control: auto-enable"

**完整文档**：[§9.22 远程控制 — 移动端访问](ultimate-guide.md#922-remote-control-mobile-access) | [安全说明](security-hardening.md#remote-control-security)

---

## 任务管理（v2.1.16+）

**两套系统可供选择：**

| 系统                   | 何时使用       | 持久化                      |
| -------------------- | ---------- | ------------------------ |
| **任务 API**（v2.1.16+） | 跨会话项目、依赖关系 | ✅ 磁盘（`~/.claude/tasks/`） |
| **TodoWrite**（旧版）    | 简单单会话      | ❌ 仅会话内                   |

### 任务 API 命令

```bash
# 启用跨会话持久化
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude

# Claude 内部：创建任务层级
> "为认证系统创建带依赖关系的任务"

# 稍后恢复（新会话）
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude
> "TaskList 查看当前状态"
```

**核心能力：**

- 📁 **持久化**：跨越会话结束、上下文压缩
- 🔗 **依赖关系**：任务 A 阻塞任务 B
- 🔄 **多会话**：向多个终端广播状态
- 📊 **状态**：pending → in_progress → completed/failed

**⚠️ 限制**：TaskList 仅显示 `id`、`subject`、`status`、`blockedBy`。
如需 `description`/`metadata` → 对每个任务使用 `TaskGet(taskId)`。

**提示**：将关键信息放在 `subject` 中以便快速浏览。

**迁移标志**（v2.1.19+）：

```bash
# 恢复旧的 TodoWrite 系统
CLAUDE_CODE_ENABLE_TASKS=false claude
```

**→ 完整工作流程**：[guide/workflows/task-management.md](../workflows/task-management.md)

---

## 黄金法则

1. **接受前务必审阅 diff**
2. **在上下文达到临界点前使用 `/compact`**（>70%）
3. **请求要具体**（WHAT、WHERE、HOW、VERIFY）
4. **复杂/高风险任务先用计划模式**
5. **为每个项目创建 CLAUDE.md**
6. **每个完成的任务后频繁提交**
7. **了解发送了什么** — 提示词、文件、MCP 结果 → Anthropic（[选择退出训练](https://claude.ai/settings/data-privacy-controls)）

---

## 快速决策树

```
简单任务       → 直接问 Claude
复杂任务      → 先用任务 API 规划
高风险更改      → 先用计划模式
重复性任务    → 创建智能体或命令
上下文满了      → /compact 或 /clear
需要文档         → 使用 Context7 MCP
深度分析     → 使用 Opus（默认开启思考）
```

---

## 常见问题快速修复

| 问题                  | 解决方案                                                         |
| ------------------- | ------------------------------------------------------------ |
| "Command not found" | 检查 PATH，重新安装：`curl -fsSL https://claude.ai/install.sh \| sh` |
| 上下文过高（>70%）         | 立即 `/compact`                                                |
| 响应变慢                | `/compact` 或 `/clear`                                        |
| MCP 不工作             | `claude mcp list`，检查配置                                       |
| 权限被拒绝               | 检查 `settings.local.json`                                     |
| 钩子阻塞                | 检查钩子退出码，审查逻辑                                                 |

**健康检查脚本**（保存并运行）：

```bash
# macOS/Linux
which claude && claude doctor && claude mcp list

# Windows PowerShell
where.exe claude; claude doctor; claude mcp list
```

---

## 成本优化

| 模型       | 用途                   | 成本  |
| -------- | -------------------- | --- |
| Haiku    | 简单修复、审阅              | $   |
| Sonnet   | 大部分开发工作              | $$  |
| Opus     | 架构设计、复杂 Bug          | $$$ |
| OpusPlan | 计划（Opus）+ 执行（Sonnet） | $$  |

**提示**：使用 `--add-dir` 允许工具访问当前工作目录外的目录

---

## 社区工具

| 工具                     | 用途               | 安装                                                                                  |
| ---------------------- | ---------------- | ----------------------------------------------------------------------------------- |
| **ccusage**            | 成本追踪与报告          | `bunx ccusage daily`                                                                |
| **RTK**                | Token 缩减（60-90%） | `brew install rtk-ai/tap/rtk` 或 `cargo install rtk` · [官网](https://www.rtk-ai.app/) |
| **claude-code-viewer** | 会话历史 UI          | `npx @kimuson/claude-code-viewer`                                                   |
| **Entire CLI**         | 会话检查点 + 治理       | [entire.io](https://entire.io)（2026 年 2 月）                                          |

> **Entire CLI**：前 GitHub CEO 打造的智能体原生平台，支持可回退检查点、审批门控、审计追踪。适用于合规场景（SOC2、HIPAA）或多智能体工作流程。

---

## 搜索工具快速参考

快速决策（5 秒）：精确文本 → `rg` | 精确名称 → `rg`/Serena | 概念 → grepai | 结构 → ast-grep

| 任务                     | 工具         | 命令                               |
| ---------------------- | ---------- | -------------------------------- |
| "查找 TODO 注释"           | `rg`       | `rg "TODO"`                      |
| "查找认证代码"               | `grepai`   | `grepai search "authentication"` |
| "谁调用了 login？"          | `grepai`   | `grepai trace callers "login"`   |
| "获取文件结构"               | `Serena`   | `serena get_symbols_overview`    |
| "缺少 try/catch 的 async" | `ast-grep` | `ast-grep "async function $F"`   |

速度：`rg`（约 20 毫秒） → Serena（约 100 毫秒） → ast-grep（约 200 毫秒） → grepai（约 500 毫秒）

> 完整工作流程：[workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md)

---

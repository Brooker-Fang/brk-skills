# brk-skills

Brooker 的私人 Claude Code skill 仓库。每个顶层目录是一个 skill（含 `SKILL.md` + 可选 `templates/`）。

## 启用方式

Claude Code 从 `~/.claude/skills/` 发现用户级 skill。把本仓某个 skill 软链或拷过去即可：

```bash
# 软链（推荐，改了即时生效）
ln -s "$(pwd)/spec-harness" ~/.claude/skills/spec-harness        # macOS / Linux
# Windows PowerShell（管理员）
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\spec-harness" -Target "<repo>\spec-harness"

# 或直接拷贝
cp -r spec-harness ~/.claude/skills/
```

启用后在 Claude Code 里 `/spec-harness` 显式唤起，或在描述匹配时自动触发。

## skills

| skill | 用途 |
|-------|------|
| [spec-harness](spec-harness/) | 用 spec-driven + harness 协作模式起一个新产品：准备阶段管道（PRD→KB→SRS→架构→任务卡）+ 轻量但真确定性的强制层（保护路径 git 钩子、产物派生 done、按 agent 分事件流水、出题独立、一卡一会话）。面向多人/多 agent。 |

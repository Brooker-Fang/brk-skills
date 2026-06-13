<!-- 本文件由 spec-harness skill 铺设；与 AGENTS.md 必须同内容（单一事实源）。 -->

# CLAUDE.md — {{PRODUCT}}（spec-driven + harness 协作版）

> 一切工作从「领一张任务卡」开始、以「提交 + DoD 报告」结束；规则尽量活在工具/钩子里。
> 本文件与 `AGENTS.md` 同源同内容，不一致请同时改。

## 入口指引

1. **开始干活 = 领一张 `tasks/` 下 `owner` = 你、且未 done 的卡**（按文件名序号顺序）。
2. 动手前先复述「我理解的范围与 DoD」；超出 `scope` 的发现**不许顺手做**，登记后另立卡。
3. 引用 spec 用精确条款 ID / 文件位置，不靠记忆。
4. 完成 = 本地质量门全绿 → 写 `reports/<卡id>.md` DoD 报告 → 提交，message 带 `[card:<id>] [agent:<你的名字>]`，然后**结束会话**（一卡一会话）。
5. 机器身份：`git config --local team.agent <名字>`（每台机器一次；commit 署名与领卡都用它）。

## 目录约定

- `docs/` 设计与规约（`prd/` / `kb/` / `srs.md` / `architecture.md`）——**保护路径**
- `tasks/` 任务卡（YAML，一卡一文件，序号前缀控顺序）
- `contracts/` 共享数据契约（冻结后**保护路径**）
- `tests/contract/` 条款测试（出题产物，冻结后**保护路径**）；`tests/unit/`；`tests/fixtures/`（每个带 `_source_ref`）
- `reports/` DoD 报告（done 状态的派生依据之一）
- `logs/` 事件流水 `events-<agent>-<card>.jsonl`

## 禁改清单（保护路径）

见 `.specharness/protected.txt`。改动其中文件的提交**必须**在 commit message 加一行 `OVERRIDE: <原因>`（commit-msg 钩子强制留痕）。

## 阅读序

PRD → KB → `docs/srs.md` → `docs/architecture.md`。按任务卡 `must_read` 字段精确加载，不全文通读。

## 纪律

- **一卡 = 一个会话 = 一（组）commit**；换任务必开新会话（防长上下文污染）。
- 卡住约 30 分钟无实质进展 → 停手，登记后找人或换路。
- **禁止绕过式修复**：不许为让测试变绿注释断言、加 skip、改条款测试。
- 出题方 ≠ 实现方：条款测试由不实现该模块者在实现前写好并冻结。
- **状态从磁盘可重建**：新会话靠任务卡 + `logs/` + `git log` 恢复上下文，不依赖"记得"。

## 红旗（仍须问人）

- 删除文件、调整规范或目录结构
- `.env` / 密钥 / token / 凭证操作
- `git push --force` / rebase 已推送分支
- 对外发布（部署、发文章等）

---
name: spec-harness
description: >-
  Bootstrap a new product/project with a spec-driven + harness collaborative
  methodology for multi-agent / multi-human teams. Use when the user wants to
  START a new product this way, or references "spec-harness", "spec-driven
  harness", "the diggy/hx workflow", or "用这套协作模式开新项目". Drives the
  prep-phase pipeline (PRD -> knowledge base -> machine-checkable SRS ->
  architecture -> task cards) and scaffolds a lightweight but real enforcement
  layer (CLAUDE.md/AGENTS.md, task-card convention, git protected-path hook,
  artifact-derived "done" state, per-agent event logs, out-of-band test
  authoring, one-card-one-session discipline). Not for single quick scripts.
---

# spec-harness — 用 spec-driven + harness 模式起一个新产品

这套方法论的内核:**当开发者是 AI(且多人/多 agent 并行)时,质量从「靠人盯」重构为「靠机制咬」——把约束做进工具、做进流程时序、做进无法伪造的产物派生里,而不是写成更多叮嘱。**

它有两层,本 skill 两层都铺:

- **确定性层(guarantee)**:git 钩子拦保护路径、done 从产物派生、按构造避开协作冲突 —— 违规结构上做不到。
- **引导层(playbook)**:准备阶段管道 + 纪律 —— 指导 agent 怎么想清楚、怎么施工。

> 关键判断:skill 本身只是「给 AI 的叮嘱」(inferential)。所以本 skill 的**职责是把它自己装不下的确定性层安装进新仓库**(git 钩子等),而不是只留一份流程说明。

## 适用与不适用

- **适用**:多人/多 agent 协作、有一定复杂度、值得先把规约想清楚的产品。
- **不适用**:一次性脚本、单人快速验证 —— 这套准备成本会变成杀鸡用牛刀,直接写即可。
- 不确定时先问用户规模与寿命,再决定要不要全套。

---

## 执行流程(按阶段走,不要跳到写业务代码)

### 阶段 0 — 对齐与身份

1. 确认用户要的是**完整方法论**(重准备),而非快速原型。若是后者,建议退化为轻量版或直接写。
2. 确认协作规模:几人、几台机器、几种 agent。多 agent 时确立机器身份约定:`git config --local team.agent <名字>`(每台机器一次;commit 署名与领卡都用它)。
3. 确认分支与集成模型(默认:每张卡一个 git worktree + 分支,done 时 rebase 集成分支后直推)。

### 阶段 1 — 准备阶段管道(先想清楚,产物全部落盘进 `docs/`)

按顺序产出,每步都是一份提交进仓库的文档,**后一层引用前一层、不复述**:

1. **PRD**(`docs/prd/`):解决什么问题、给谁用、什么算成功。**不写系统行为**。
2. **知识库 KB**(`docs/kb/systems/` 环境事实 + `docs/kb/workflows/` 用例澄清):AI 没有老员工的脑子,这层要厚。环境/字段/接口/关键用例怎么走、失败模式。
3. **SRS**(`docs/srs.md`,骨架见 `templates/SRS-skeleton.md`):把"必须为真且可验证"的部分契约化成 schema / 规则 / 错误类型。**每条约束打执行层标签** `[machine]`(可机械强制 → 必须有校验代码或测试)/ `[prompt]`(指导 → 进 system prompt)/ `[eval]`(行为质量 → 进 golden case)。这张标签表本身就是漏项检测表。给每条一个稳定 ID(如 `G-RT-1`)。
4. **architecture**(`docs/architecture.md`):模块拆解、边界、依赖图。这是任务卡拆分的依据 —— **拆分是设计期的人类动作,不让 agent 运行时自由拆**。
5. **任务卡**(`tasks/*.yaml`,模板见 `templates/task-card.yaml`)。每张含:
   - `id` / `goal` / `scope`(**负向边界**,写明"仅改 X、不碰 Y")/ `owner`(领卡归属)/ `deps`(依赖的卡或冻结点)/ `must_read`(精确 spec 节,新会话只加载这些)/ `dod`(完成定义)/ `covers`(覆盖的 SRS 条款 ID)。
   - 文件名加序号前缀(`30-xxx.yaml`)控制领卡顺序。
   - 粒度 ≈ 一个子模块、0.5–2h。

把数值常量收成**一张集中参数表**(`params` 模块或 `docs/params.md`),业务代码禁止裸数值;调参改表不改散文。

### 阶段 2 — 铺确定性层(强制,做进工具)

用 `templates/` 里的文件铺进新仓库,按需改名/改内容:

1. **`CLAUDE.md` + `AGENTS.md`**(用 `templates/CLAUDE.md`):**同一份内容**(单一事实源;CLAUDE.md 给 Claude Code,AGENTS.md 给 Codex/其它 agent,内容必须一致)。含入口指引、保护路径清单、阅读序、纪律、红旗。
2. **保护路径 git 钩子**(用 `templates/commit-msg-protected.py` + `templates/protected.txt`):把 `protected.txt` 放到新仓 `.specharness/protected.txt`,脚本拷到 `.git/hooks/commit-msg`(POSIX 加可执行位;Windows 确保 python 在 PATH)。冻结后的 SRS/架构/contracts/条款测试改动,提交信息无 `OVERRIDE: <原因>` 即拦死。**连 `protected.txt` 自身也保护**(防删清单绕过)。
3. **产物派生 done(无可变状态字段)**:一张卡 done 的判据 = `reports/<id>.md`(DoD 报告)存在 **且** `git log --grep="[card:<id>]"` 命中。任务卡 YAML 里**不存 status**。伪造状态 = 伪造全套产物。
4. **按 agent 分事件流水**:每张卡每个 agent 的事件写 `logs/events-<agent>-<card>.jsonl`(一行一事件 `{ts,event,payload}`)。**按 (agent, card) 分文件 → 多人并行零合并冲突**(冲突按构造避开,而不是事后解决)。
5. **worktree 隔离**:每张卡在独立 git worktree 里干,done 时 rebase 集成分支后直推。多人同机互不踩。

### 阶段 3 — 测试与实现分离(质量主机制)

- **出题方 ≠ 实现方**:每个模块的条款测试,由**不实现该模块的人、在实现存在之前**从 SRS 写好并冻结(进保护路径)。spec 分歧表现为客观红测试(回 SRS 原文可仲裁),不表现为 review 意见。
- 出题质量四防线:漏题(条款覆盖差集检查)、水题(空实现上必须全红才算有效题)、错题(出题产物附「条款 ID ↔ 测试名 ↔ 断言一句话」映射表,人扫表)、私自解题(条款歧义只准上报、不准自选解读)。
- 测试不打桩:用产品自带的 mock 后端(与真实后端同签名);fixture 不许编,从 KB 提取并标 `_source_ref`。

---

## 日常循环(铺好后每个人/agent 怎么干)

写进 CLAUDE.md,让每个会话照做:

1. **领卡**:挑一张 `owner` = 自己、未 done 的卡(按文件名序号顺序);进它的 worktree。
2. **复述**:动手前先复述「我理解的范围与 DoD」,对照卡的 scope/dod。
3. **施工**:只在 scope 内改;`must_read` 之外不通读全仓。
4. **完成**:本地质量门全绿 → 写 DoD 报告 → 提交,commit message 带 `[card:<id>] [agent:<名字>]`。
5. **一卡 = 一会话 = 一(组)commit**;换任务必开新会话(防长上下文污染)。

### 铁律(写进 CLAUDE.md「纪律」节)

- **超范围发现只登记、不顺手做**:记一条 escalate 事件 + 另立卡。
- **禁止绕过式修复**:不许为让测试变绿注释断言、加 skip、改条款测试(保护路径会拦)。
- **保护路径破例必留痕**:commit message 加 `OVERRIDE: <原因>`。
- **红旗仍须问人**:删文件、改规范/目录结构、凭证/密钥操作、force push、对外发布。
- **状态从磁盘可重建**:新会话靠任务卡 + 事件日志 + git log 恢复上下文,不依赖"记得"。

---

## 确定性 vs 叮嘱(铺设时的判断尺)

每加一条约束先问:**它能做成"跑起来的代码保证",还是只能"指望 agent 听话"?**

- 能做成保证的(保护路径、done 派生、冲突按构造避开、schema 校验)→ **做进钩子/代码/产物结构**。
- 只能指望的(prompt 措辞、叙述质量)→ 进 prompt + 用 eval 行为断言**间接**兜底,并标 `[prompt]`/`[eval]` 隔离起来,别假装它是保证。

这条尺贯穿全程:本 skill 给的是引导(叮嘱),它装下的钩子才是保证 —— 两者配套,缺了钩子那半,整套会退化成又一份没人强制执行的最佳实践文档。

---

## 与现成工具的关系

前端的 spec→tasks 生成可以用 **GitHub Spec Kit / OpenSpec** 等现成工具(有维护、生态好);本 skill 的差异化价值在**执行纪律层**——多人/多 agent 协作的冲突按构造避开、产物派生防作弊、出题独立性——这层现成工具普遍不深做。理想是:**现成工具做 spec 前端 + 本 skill 这套强制/协作层叠加在上**。

## 模板清单(`templates/`)

- `CLAUDE.md` — 项目入口指引 / 保护路径 / 阅读序 / 纪律(同内容复制一份为 AGENTS.md)
- `task-card.yaml` — 任务卡字段模板
- `commit-msg-protected.py` — 保护路径 commit-msg 钩子(无依赖,跨平台)
- `protected.txt` — 保护路径清单(含自身,防绕过)
- `SRS-skeleton.md` — SRS 起步骨架(含执行层标签说明)

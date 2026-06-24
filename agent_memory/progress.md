# Task Progress

## Current Goal

- 目标：排查并修正 `short-video-storyboard` 发布后被协作者使用时输出过短、格式不固定的问题。
- 成功标准：明确原因；将 `故事核心`、逐镜头块格式、累计时间段、禁止四列表格摘要、镜头字段完整度等硬约束同步进发布 skill 本体和模板引用；移除已废弃的中文问卷残留；把 Hook 审查机制拆为 reference 并要求每次审查后沉淀新案例；完成 skill 验证。
- 范围边界：只处理 `short-video-storyboard` 的格式约束和必要项目记录；不改 HTML skill、首帧图 skill 或历史输出文件。
- 停止条件：skill 文件可解释，校验通过，Git diff 可审查。
- 验证方式：`rg` 检索关键规则、`git diff --check`、`quick_validate.py`。

## Status

- 当前状态：已确认主要原因是强格式规则分散在项目级 `AGENTS.md` / `docs/storyboard-workflow.md`，但发布 skill 自身约束偏软；协作者只触发 skill 时容易退化成短摘要表。
- 已完成：更新 `.codex/skills/short-video-storyboard/SKILL.md`、`references/storyboard-template.md`、`agents/openai.yaml`；新增 `references/hook-review.md` 并把 Hook 细则和案例库迁入；新增 Hook 案例库维护规则；新增 `docs/session-summaries.md` 的 2026-06-24 workflow 记录；移除 `short-video-storyboard` 中的旧中文问卷和模板提问卡；`git diff --check` 通过；`quick_validate.py` 在 UTF-8 模式下通过。
- 下一步：提交并推送本轮 skill hardening 变更，让协作者拉取更新。

## Notes

- 阶段变化：项目发布后进入协作者使用反馈修正阶段。
- 当前有效 skill 集合：`short-video-storyboard`、`storyboard-html-delivery`、`storyboard-first-frame-images`、`aig-image-gen`。
- 经验：不能只依赖项目级 AGENTS/README 约束发布后的行为；用户最在意的交付格式必须进入被触发 skill 的 `SKILL.md` 和模板引用。
- 经验：废弃的 brief 收集方式也必须从 skill 本体和引用模板同步删除，否则协作者会继续看到旧问卷。
- 经验：会持续增长的审查规则和案例库应放在 `references/`，`SKILL.md` 只保留加载索引和强制更新规则，避免主 skill 越写越长。

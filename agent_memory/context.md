# Project Context

## Project Snapshot

- 项目名称：
- 主要目标：
- 当前阶段：

## Architecture And Conventions

- 关键目录：
- 主要技术栈：
- 既有约定：

## Important Decisions

- 决策：
- 原因：
- 日期：

## Current Effective Context

- 当前有效背景：短视频分镜工作流分为分镜、HTML、首帧图三个职责；TK 太阳能户外灯串项目位于 `outputs/2026-06-23-tk-solar-string-lights/`。
- 需要持续记住的限制：首帧图完成后默认开启子 agent 视觉 QA；只有任务里有明确产品参考图或产品结构要求时，才审查产品大小比例是否在所有分镜图中一致、产品结构是否符合参考图。没有产品参考时不做产品审查，只审查首帧规则、分镜匹配、人物变形、姿势动作、场景连续性、光线和因果。局部失败优先用 `gpt-image-2` edit 生成候选，候选过审后替换稳定 `shot-XX-*.png`，最终交付目录不保留失败候选、mask、crop 或草稿文件。
- 无缝转场依据：2026-06-23 已把用户提供的动态设计转场逻辑整理为 `docs/transition-logic.md`。以后写“无缝转场”或“空镜转场”时，按遮挡转场、动势匹配转场 / match cut、前后承接转场、无缝转场、空镜转场分类，并写清共享视觉锚点与转场目的。
- Brief 面板方向：`outputs/storyboard-brief-selector.html` 已改为社媒短视频创意 Brief。面板保留基础信息、核心卖点、场景、平台、视频时长，并以开头钩子、内容结构、留存节奏、转场技巧、拍摄技巧、声音与包装作为主要输入；生成 brief 默认要求先给内容钩子、节奏、转场、拍摄剪辑建议，再写分镜。

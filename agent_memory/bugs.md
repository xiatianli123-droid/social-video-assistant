# Bugs And Risks

## Active Issues

- 问题：早期分镜存在钩子偏弱或旧标准写法，主要表现为开场只建立氛围/环境，缺少异常、冲突、反差或强信息缺口。
- 影响：短视频前 0.5-3 秒停留理由不足，广告卖点虽完整但滑动平台吸引力偏弱。
- 状态：已识别，Hook 审查机制已从 `SKILL.md` 拆到 `references/hook-review.md`，尚未改稿。
- 下一步：如继续处理，优先修订 outputs/2026-05-14-string-lights、outputs/2026-05-15-fengshan-deng、outputs/2026-05-15-downlight 的镜头 1 和故事核心。

## Risks

- 风险：发布后的协作者环境只触发项目 skill，但没有完整加载项目级 `AGENTS.md` / `README.md` / `docs/storyboard-workflow.md`，导致分镜输出退化成简短摘要表。
- 触发条件：格式硬规则只写在项目文档里，`short-video-storyboard` 的 `SKILL.md` 和模板引用没有明确禁止宽表/四列摘要表，也没有把 `故事核心`、逐镜头块、累计时间段写成必选。
- 缓解方式：2026-06-24 已把这些硬规则同步进 `short-video-storyboard` 的 `SKILL.md`、`references/storyboard-template.md` 和 `agents/openai.yaml`；后续发布前优先检查 skill 本体是否包含关键交付约束。

- 风险：旧版文字问卷残留在发布 skill 中，协作者看到后可能绕过共享 brief 面板。
- 触发条件：`short-video-storyboard` 的 `SKILL.md` 或 `references/storyboard-template.md` 保留“默认中文问卷 / 生成前提问卡 / 先问 6 个问题”等旧内容。
- 缓解方式：2026-06-24 已删除旧中文问卷和模板提问卡，改为 brief 不完整时统一打开 `outputs/storyboard-brief-selector.html` 并等待用户发回生成简报。

- 风险：只在 skill 中写“强 hook”但不要求每个镜头声明广告功能，后续脚本可能又回到慢铺垫。
- 触发条件：用户只给产品名或泛生活方式方向，且未强制首镜动作化。
- 缓解方式：把钩子检查落为硬标准：首帧已在动作中、0.5 秒可见问题/异常/结果、镜头 1 不只建立环境、镜头 2 必须有触发点或反转推进。

- 风险：首帧图场景和人物通过但产品配件局部变形，或同一产品在不同分镜中的大小比例、结构细节不一致，例如灯座、挂钩、遥控器按钮状态不符合产品参考。
- 触发条件：任务提供了产品参考图或明确产品结构要求，但首帧生成或编辑只按氛围/场景相似度通过。
- 缓解方式：首帧 QA 默认开启子 agent 视觉审查；有产品参考时重点检查产品大小比例是否所有分镜一致、产品结构是否符合用户参考图。无产品参考时跳过产品审查，只检查首帧规则、分镜匹配、人手姿势、场景连续和因果；局部失败优先用 `gpt-image-2` edit 生成候选，候选过审后再替换稳定文件，并清理失败候选。

- 风险：首帧 QA 可能把文字碎片、标签痕迹、UI/界面残影、角色表/五官参考污染或拼贴残影本身误判为失败。
- 触发条件：AIG 参考图或首帧图出现轻微伪文字、标签式标记、界面式残留、角色参考表残影，但这些残影没有遮挡主体、没有改变分镜含义，也没有破坏人物/产品/道具结构。
- 缓解方式：已将规则同步到 `AGENTS.md` 与 `docs/storyboard-workflow.md`：这类残影不作为独立失败来源；只有当它们违背分镜、遮挡关键信息、造成人物/产品/道具变形或冲突用户明确要求时才判失败。构图检查是独立的摄影逻辑检查，不包含 UI/模板残留判断；仅限：画面是否仍像一个连贯镜头空间；前景/中景/背景是否能连接成分镜所述场景；主要主体透视和光线是否兼容；必需视觉焦点是否可识别。

## Resolved

- 已解决事项：2026-06-24 已修正 `short-video-storyboard` 发布后格式约束偏软的问题：skill 本体现在要求 `故事核心`、逐镜头块、固定字段顺序、累计时间段、禁止四列摘要表和更完整的单镜执行信息；模板引用和 `agents/openai.yaml` 已同步。
- 已解决事项：2026-06-24 已移除 `short-video-storyboard` 中过时的“默认中文问卷”和模板“生成前提问卡”，brief 不完整时统一使用共享 brief 面板。
- 已解决事项：2026-06-24 已把 Hook 审查细则从 `short-video-storyboard/SKILL.md` 拆到 `references/hook-review.md`；`SKILL.md` 只保留索引，并要求每次 Hook 审查或改写后追加新案例到该 reference。
- 已解决事项：2026-06-24 已为 `references/hook-review.md` 增加案例库维护规则：超过 20 条整理、每类最多 3-5 条代表案例、重复经验提炼进规则、历史材料按需归档。
- 已解决事项：2026-06-24 已将具体生活方式案例改为 `references/lifestyle-product-storyboard.md` 纯抽象生活方式产品分镜经验，只保留结构、证明方式和误用提醒。
- 已解决事项：2026-06-24 已删除 `short-video-storyboard/references/storyboard-template.md` 中误放的 `AIG 首帧生成规则`，并清理 `shot-language.md` 中越界的首帧/AIG prompt 表述；首帧生成规则只归 `storyboard-first-frame-images`。
- 已解决事项：本轮完成 9 份既有 storyboard.md 的钩子落实度审查；已将“四问不外显、只输出画面内容”的 hook 审查机制固化进 short-video-storyboard skill。
- 已解决事项：2026-06-23 已把首帧图默认开启子 agent 视觉 QA、产品参考存在时才做产品跨分镜大小比例和参考图结构一致性审查、无产品参考时只审首帧规则、候选先审后替换、局部失败优先 edit、交付目录清理失败候选的方法同步进 `storyboard-first-frame-images` 和 `docs/storyboard-workflow.md`。
- 已解决事项：2026-06-23 已把共享 brief 面板从偏运营项重构为社媒创意导向，新增开头钩子、内容结构、留存节奏、转场技巧、拍摄技巧、声音与包装，并要求 brief 先给社媒创意建议再写分镜，降低后续输入只停留在类目/受众/情绪标签的风险。

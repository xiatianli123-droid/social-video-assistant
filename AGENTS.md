# Agent Instructions For H:\TVC

Use these rules when working in this project.

## Skill Boundaries

- Use `short-video-storyboard` for storyboard writing and physical-world continuity checks.
- Use `storyboard-html-delivery` for creating or updating `storyboard.html`.
- Use `storyboard-first-frame-images` only after the user confirms first-frame image generation.
- When `storyboard-first-frame-images` performs actual raster generation or editing, use `aig-image-gen` as the image-generation skill.
- For `storyboard-first-frame-images`, every shot image must use only `reference-character-3view-face.png` and `reference-scene-concept.png` as image inputs. Do not pass any generated `shot-*.png` image as a later image reference; keep shot continuity through prompt text, storyboard causality, stable wardrobe, props, and scene layout.
- For `storyboard-first-frame-images`, if the same object appears in two or more storyboard shots, add a compact object inventory to the character reference sheet prompt. Lock each recurring object's color, material, size, shape, worn/carried position, and which character uses or carries it.
- For `storyboard-first-frame-images`, character master/reference sheet prompts must include a hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
- For `storyboard-first-frame-images`, the scene concept reference must cover every recurring location and every product state used by the storyboard, such as lights-off/lights-on, open/closed, dry/wet, installed/uninstalled, or before/after states. If the storyboard depends on multiple states, include them in one continuity reference before generating shots.
- For `storyboard-first-frame-images`, `reference-scene-concept.png` must be a no-people environment reference. It should include wide/global view, medium view, and close-up view for each main recurring location or product-zone when practical, so later shots have camera-scale continuity without introducing characters into the scene reference.
- Do not overwrite an accepted reference image based on assistant-only uncertainty. If a reference image needs refinement after inspection, create a temporary candidate first and replace the stable `reference-*.png` file only after the user accepts it or the image is objectively unusable against explicit requirements.

Do not collapse these responsibilities back into one workflow.

## Summary Log

- Keep versionable workflow summaries in `docs/session-summaries.md`.
- When generating or updating a project/workflow summary in conversation, append or update a dated section in `docs/session-summaries.md`.
- Each summary entry must include the date, affected project path, key rule or asset changes, current output status, and next required step when applicable.

## Required Flow

1. If the user has provided only a product name or an incomplete brief, open `outputs/storyboard-brief-selector.html` for brief intake, ask the user to send back the generated brief, and stop. Do not write a storyboard, create a project output directory, or generate HTML until the user provides the completed brief or explicitly asks to use defaults.
2. Once the brief is complete, write the storyboard script first, and include the script in the conversation response rather than only linking the HTML.
3. Generate or update HTML delivery.
4. Open the generated `storyboard.html` for preview when possible.
5. Ask for first-frame confirmation directly in the conversation with three choices: "需要生成首帧图", "暂不生成首帧图", or "先修改分镜再决定". Do not use an HTML page for this confirmation.
6. Generate first-frame images only after confirmation.
7. After all first-frame images are generated, review every image against its storyboard row before final delivery. If any visible detail conflicts with the storyboard description, even one mismatch, treat that image as unusable and regenerate it.
8. Update the same `storyboard.html` only after the full first-frame set is generated or regenerated and has passed review. Do not update HTML for reference-only changes or partial shot-image progress.

HTML is mandatory whether images are generated or not.
Open local HTML preview files automatically without asking again once the environment has a reusable `Start-Process` approval. If that approval is not available yet, request it once with a reusable prefix rule. This applies to brief intake and storyboard preview, not first-frame confirmation.

Always provide a short `故事核心` summary for storyboard deliveries and meaningful storyboard revisions. Put it in the conversation response, include it in `storyboard.md`, and show it in `storyboard.html`. The story core should be a compact reference line that explains the ad's causal arc, selling-point proof, and ending/payoff. Example pattern: `热闷让泳池派对从庭院流失，主人一键开启风扇灯，清风和暖光把人重新拉回户外，最后用正常音量聊天证明低噪。`

The shared brief selector separates `平台` and `视频时长`. Duration options are `15秒`, `20秒`, `30秒`, and `60秒`, defaulting to `15秒`.

Storyboard shot durations are flexible. Assign duration by advertising function, information load, and platform rhythm; short shots below `5秒` are allowed when they still make the selling point legible. For short projects, adjust shot count and duration together instead of padding weak shots.

`storyboard.md` 分镜默认使用 `outputs/2026-06-03-downlight-city-hero/storyboard.md` 的逐镜头块格式，而不是宽 Markdown 表格。每个镜头按固定字段顺序书写：`镜头 N`、`时长：`、`景别：`、`运镜：`、`运镜逻辑：`、`画面描述：`、`文案旁白：`、`音效配乐：`。`时长` 必须写累计时间段，例如 `0-2.5秒`、`2.5-5秒`、`5-8秒`，而不是单镜时长 `2.5 秒`。Do not add `执行备注`, `首帧图方向`, or `首帧方向`.

In the `文案旁白` field, write narration or character dialogue in English by default unless the user explicitly asks for Chinese copy. Keep the storyboard explanations and field labels in Chinese. For any voiced line, include a stable voice anchor in the same field, such as `音色：... "English line"`; repeat the same narrator voice anchor across all narrator lines, and keep each recurring character's speaking voice consistent across shots.
Do not write screen copy in `文案旁白` by default. Use narration or character dialogue only, unless the user explicitly asks for on-screen text/subtitles.

## Continuity Standard

Before finalizing a storyboard or image prompt, check:

- Weather
- Time
- Space
- People and wardrobe
- Props
- Product state
- Lighting and color system
- Event causality

Every new visual element must have a source. It must be established earlier, caused by the current shot, or normal for the scene. Do not add a selling-point proof element that breaks the physical world.

## Short-Video Rhythm Standard

Short-video storyboards must not feel like a slow excerpt from a longer film. Every shot must create an immediate information gain and make the selling point legible quickly.

- Avoid shots whose main action is only "a person walks over", "they see each other", or "they slowly move closer". Character movement is only a carrier; the selling-point change is the purpose.
- Write trigger points and result moments instead of full processes. Prefer: pre-trigger need -> trigger moment -> result moment -> product/scene memory.
- Each shot's opening frame should already be in action. Example: the napkin is already lifting, hair is already moving, the drink is already at the handoff point, or the fan light is already the hero.
- Do not let a 15-second ad carry too much relationship plot. Character smiles, normal-volume conversation, hair/fabric movement, and people staying outdoors should all serve product proof.
- Assign one clear advertising function to every shot: hook/pain point, core selling point, reaction proof, or product memory/purchase reason.
- Use editing jumps to compress real movement. Consistency means the space, people, props, product, and lighting remain coherent; it does not mean every walk, glance, or approach must be shown in full.
- Practical check: if viewers cannot understand what the shot is selling within the first 0.5 seconds, rewrite the shot.

## Transition Logic Reference

When the user asks for seamless transitions or 空镜转场, use `docs/transition-logic.md` as the project reference. Choose the transition by purpose, not decoration:

- 遮挡转场：use foreground occlusion or same-direction motion to hide the cut; match the next shot's direction, speed, or covered area.
- 动势匹配转场 / match cut：match movement direction, visual content, angle, or action between shots, such as down/up motion, rotation, object recognition, similar angle, or continuous action.
- 前后承接转场：carry the same action, object, framing, or UI/layout logic across the cut so the next shot feels like a natural continuation.
- 无缝转场：use dissolve cut when two shots can crossfade through similar texture, light, color, or shape; use invisible cut when shadow, darkness, camera whip, occlusion, or a close object hides the edit point.
- 空镜转场 / cut away：insert a relevant but not necessarily causally adjacent empty shot between two unrelated scenes to express mood, character inner state, time passage, or location reset.
- For every seamless transition, explicitly state the shared visual anchor and the reason the cut is physically legible.

## Sound Column Standard

- In `音效配乐`, write only sounds that should actually be heard in the shot.
- Keep `音效配乐` as one field, but write only the sound categories that serve the shot's main visual expression. Be concise: wide environment shots may only need `环境声`; dialogue shots should include `人声`; action or prop-focused shots may include `动作音效` or `道具声`; use `BGM` only when it supports the emotional rhythm.
- Do not write reverse instructions such as "不加某声音", "不添加某音效", or "不额外添加产品声"; omitted sounds should simply be absent.
- For quiet or low-noise products, prove quietness through grounded scene sounds, character reactions, and normal conversation volume.

## Shared Panels

- Brief intake: `outputs/storyboard-brief-selector.html`
First-frame confirmation is handled in the conversation, not through an HTML panel. Do not create one-off confirmation pages for storyboard projects.

## First-Frame Image Review Standard

After the full first-frame set is generated, perform a strict image-vs-storyboard review before treating the set as complete.

- Before shot generation, inspect both reference images against explicit user requirements. Scene references must include all storyboard-critical states, must not contain people unless the user explicitly asks otherwise, and must include wide/global, medium, and close-up camera scales where practical. Accepted references are locked unless the user asks to change them.
- Compare each `shot-*.png` against its storyboard row for scene, time, space, people, wardrobe, props, product visibility/state, lighting, action, composition intent, and event causality.
- Excluding intentionally blurred faces, any mismatch with the storyboard description makes the image unusable. There is no tolerance for "close enough" when one visible detail contradicts the written shot.
- Visible text, label-like marks, UI-like fragments, glyph artifacts, reference-sheet pollution, character/face-sheet fragments, or collage-like interface remnants do not by themselves fail the review. Treat them as a problem only when they contradict the storyboard, obscure required visual information, deform required people/products/props, or conflict with explicit user requirements. Separately, composition checks are limited to photographic shot logic: the image no longer reads as one coherent shot space, foreground/midground/background cannot connect into the described scene, major subjects use incompatible perspective or lighting, or the required visual focus is no longer identifiable within the shot.
- Regenerate unusable images before updating final delivery. Do not mark the first-frame set complete until every image passes.
- When regenerating a shot, create a temporary candidate only for inspection. Once accepted, automatically replace the original `shot-XX-*.png` filename and keep `storyboard.html` pointing at the original stable filename. Do not leave `-v2`, `-v3`, or other candidate files as final delivery assets unless the user explicitly asks to keep variants.

## Output Convention

Project deliveries go under:

```text
outputs/YYYY-MM-DD-<project-name>/
```

Use Beijing-date output folders. Do not save prompts by default.
Do not leave temporary prompt files, dry-run text files, scratch `.txt` files, or other assistant-only working notes in project delivery folders. If a prompt or diagnostic note is needed while retrying image generation, keep it outside the delivery directory or remove it before final handoff. Save prompt files only when the user explicitly asks to keep or export them.
Dated folders under `outputs/` are historical deliveries and are not workflow authority. When old deliveries conflict with these instructions, follow `AGENTS.md`, `PROJECT_FLOW.md`, `README.md`, and the project skills.

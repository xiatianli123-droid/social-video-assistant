# Storyboard Workflow

This document explains the three-skill storyboard workflow for `H:\TVC`.

## Overview

The workflow separates script writing, HTML delivery, and image generation:

- `short-video-storyboard` writes the Chinese storyboard and continuity analysis.
- `storyboard-html-delivery` creates or updates the final HTML page.
- `storyboard-first-frame-images` orchestrates first-frame continuity only after explicit conversation confirmation. It creates a character reference sheet and scene concept reference, then uses only those two images as inputs for every storyboard shot. It uses `aig-image-gen` for actual raster generation or editing.

## Standard Flow

1. Collect or generate a brief.
   - Automatically open `outputs/storyboard-brief-selector.html` when the brief is incomplete or the user wants click-to-confirm intake.
   - If the user has provided only a product name or an incomplete brief, ask them to send back the generated brief and stop before writing a storyboard, creating a project output directory, or generating HTML, unless they explicitly ask to use defaults.
   - The shared panel is social-video oriented: after basic product information, it collects opening hook, content structure, retention rhythm, transition technique, filming technique, and sound/packaging choices.
   - The shared panel separates `平台` from `视频时长`; duration choices are `15秒`, `20秒`, `30秒`, and `60秒`, with `15秒` selected by default.
   - Briefs generated from the panel should ask for social creative recommendations first: content hook, retention rhythm, transition idea, and filming/editing suggestions before the storyboard.
2. Write the storyboard.
   - Output creative direction, storyboard shot blocks, and design analysis.
   - Include a compact `故事核心` summary in the conversation response, `storyboard.md`, and `storyboard.html`. It should state the causal arc, selling-point proof, and ending/payoff in one short reference paragraph.
   - Shot durations are flexible. Assign duration by advertising function, information load, and platform rhythm; shots below `5秒` are allowed when the selling point remains legible.
   - Include the storyboard script in the conversation response, not only in HTML.
   - Enforce short-video rhythm: every shot must reveal a new selling-point-related information gain within the first 0.5 seconds.
   - Write trigger points and result moments rather than complete process beats. Avoid shots whose main content is only a person walking over, seeing someone, or slowly moving closer.
   - Make each opening frame already active: hair or fabric is already moving, the drink is already at the handoff point, the person has already reacted, or the product is already the hero.
   - Use editing jumps to compress real movement while keeping space, people, props, product state, lighting, and color coherent.
   - Use the per-shot block format from `outputs/2026-06-03-downlight-city-hero/storyboard.md`: `镜头 N`, `时长：`, `景别：`, `运镜：`, `运镜逻辑：`, `画面描述：`, `文案旁白：`, `音效配乐：`.
   - Write `时长` as cumulative time ranges, such as `0-2.5秒`, `2.5-5秒`, and `5-8秒`, not standalone shot durations.
   - Keep the storyboard labels and analysis in Chinese, but write `文案旁白` as English narration or English character dialogue by default unless the user explicitly asks for Chinese copy.
   - For every voiced line, include the voice description in the same `文案旁白` field. Repeat the same narrator voice anchor across narrator shots, and keep each recurring character's speaking voice consistent across shots.
   - Do not write screen copy in `文案旁白` by default. Use narration or character dialogue only unless the user explicitly asks for on-screen text/subtitles.
   - Do not generate first-frame images at this stage.
3. Create HTML delivery.
   - Use `storyboard-html-delivery`.
   - Automatically open the generated `storyboard.html` for preview when possible.
   - If no images exist, keep the HTML in no-image mode without first-frame cards.
4. Ask for first-frame confirmation.
   - Ask directly in the conversation; do not use an HTML page for this step.
   - The user chooses `需要生成首帧图`, `暂不生成首帧图`, or `先修改分镜再决定`.
5. Generate images only if confirmed.
   - Use `storyboard-first-frame-images` for continuity orchestration and `aig-image-gen` for actual image generation/editing.
   - First generate and inspect `reference-character-3view-face.png` and `reference-scene-concept.png`.
   - The scene concept reference must cover every storyboard-critical product or location state before shot generation, such as lights-off/lights-on, open/closed, dry/wet, installed/uninstalled, or before/after states.
   - The scene concept reference should be an empty environment reference with no people unless explicitly requested, and should include wide/global, medium, and close-up camera scales for the main recurring location or product-zone when practical.
   - Once a reference image is accepted, treat it as locked. If refinement is needed, generate a temporary candidate for inspection and replace the stable `reference-*.png` only after user acceptance or an objective mismatch with explicit requirements.
   - If the same object appears in two or more storyboard shots, add a compact object inventory to the character reference sheet prompt. Lock color, material, size, shape, worn/carried position, and which character uses or carries each recurring object.
   - Character master/reference sheet prompts must include a hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
   - Generate shots sequentially in storyboard order, but every shot image must use only the two reference images as image inputs.
   - Do not pass any generated `shot-*.png` file into later AIG calls. Preserve shot-to-shot continuity through prompt text, storyboard causality, stable wardrobe, props, and scene layout.
6. Review the completed first-frame image set.
   - After the full set is generated, open subagent visual QA before final delivery. Compare every generated `shot-*.png` with its corresponding storyboard shot block and the other shot images in the same set.
   - Excluding intentionally blurred faces, any visible mismatch in scene, time, space, people, wardrobe, props, product visibility/state, lighting, action, composition intent, or causality makes that image unusable.
   - Enable product QA only when the task includes explicit product reference images or explicit product structure requirements. If no product reference is available, skip product-size and product-structure review and judge only first-frame rule compliance, storyboard match, human deformation, hand/body pose, scene continuity, lighting, and causality.
   - When product QA is enabled, product and accessory accuracy is a hard gate. The subagent QA must check whether product size/proportion stays consistent across all storyboard images, whether product structure matches the user reference image, product deformation, accessory shape, human deformation, hand/body pose, and whether the first frame already shows the shot's starting action or result point.
   - Visible text, label-like marks, UI-like fragments, glyph artifacts, reference-sheet pollution, character/face-sheet fragments, or collage-like interface remnants do not by themselves fail the review. Treat them as a problem only when they contradict the storyboard, obscure required visual information, deform required people/products/props, or conflict with explicit user requirements. Separately, composition checks are limited to photographic shot logic: the image no longer reads as one coherent shot space, foreground/midground/background cannot connect into the described scene, major subjects use incompatible perspective or lighting, or the required visual focus is no longer identifiable within the shot.
   - When a failure is localized, prefer `gpt-image-2` edit through `aig-image-gen edit` for that area before full regeneration.
   - When regenerating or editing a shot, create a temporary candidate for inspection first. Once the candidate passes subagent QA and main-agent sanity review, replace the original stable `shot-XX-*.png` filename and keep HTML references pointed at that stable filename. Do not leave candidate images, masks, crops, dry-run notes, `-v2`, or `-v3` variants as final delivery assets unless the user explicitly asks to keep variants.
7. Update HTML after image generation.
   - Use `storyboard-html-delivery` again to embed generated image cards and local paths.

## Physical-World Continuity Gate

Before finalizing storyboard text or image prompts, verify:

- Weather, time, location, people, wardrobe, props, product state, lighting, and color system are coherent.
- New visual elements have a source.
- Selling-point proof does not break causality.

Example: if Shots 1-3 show a dry patio, Shot 4 cannot suddenly show water droplets. To prove waterproofing, establish rain, spray, poolside use, watering, or another water source earlier.

## Short-Video Rhythm Gate

Before finalizing storyboard text or first-frame image prompts, verify:

- Each shot has one clear advertising function: hook/pain point, core selling point, reaction proof, or product memory/purchase reason.
- The shot is not just a slow process beat. Replace "a person walks over" with the result of entering the selling-point state, such as hair, clothing, napkins, drink condensation, lighting, or facial reaction already changing.
- The sequence follows a dense ad rhythm: pre-trigger need -> trigger moment -> result moment -> product/scene memory.
- Character relationships remain atmosphere, not plot. Smiles, normal-volume conversation, hair/fabric movement, and people staying outdoors must all support product proof.
- If a viewer cannot understand what the shot is selling within the first 0.5 seconds, rewrite it.

## Transition Logic Reference

Use `docs/transition-logic.md` as the local reference when designing seamless transitions, match cuts, or cutaways. Select the transition type by narrative function and shared visual anchor:

- 遮挡转场: use a foreground object, body, fabric, wall edge, camera whip, or same-direction movement to cover the edit point. The next shot should inherit a compatible motion direction, speed, or occluded screen area.
- 动势匹配转场 / match cut: connect shots through matching movement direction, visual content, camera angle, or action. Common anchors include down/up movement, rotation, object recognition, similar angle, and continuous action.
- 前后承接转场: make the second shot feel caused by the first through a continued object, action, framing, color state, or interface/layout relationship.
- 无缝转场: use dissolve cut when texture, light, color, silhouette, or product shape can blend across shots; use invisible cut when shadow, darkness, occlusion, or a near-camera object hides the edit point.
- 空镜转场 / cut away: insert a relevant empty or atmospheric shot between less-related scenes to express mood, character interiority, time passage, or location reset.

For every written transition, record the shared visual anchor and its purpose in the shot logic. A transition should not be only "cool"; it must preserve physical-world continuity or intentionally mark a readable jump.

## First-Frame Image Review Gate

After all first-frame images are generated and before final delivery, verify every image against the storyboard shot blocks:

- Reference images were inspected before shot generation and include all storyboard-critical states.
- `reference-scene-concept.png` is free of people unless explicitly requested and includes wide/global, medium, and close-up views where practical.
- Accepted reference images were not overwritten by assistant-only preference; any replacement came from user acceptance or objective mismatch with explicit requirements.
- Subagent visual QA has reviewed the final stable shot set unless subagents are unavailable; in that fallback case, report the direct-review fallback.
- The image must match the corresponding shot block's scene, time, space, people, wardrobe, props, product visibility/state, lighting, action, composition intent, and event causality.
- Ignore only intentionally blurred faces. Any other visible mismatch is a hard failure.
- Text-like fragments, label-like marks, UI-like fragments, reference-sheet pollution, character/face-sheet fragments, or collage-like interface remnants are not standalone failure sources. Judge the actual visual impact: fail only if they conflict with the storyboard, obscure required information, deform required subjects, or violate explicit user requirements. Composition checks are separate and limited to photographic shot logic: whether the image reads as one coherent shot space; whether foreground, midground, and background connect into the described scene; whether major subjects share compatible perspective and lighting; and whether the required visual focus is identifiable.
- If the task includes explicit product reference images or explicit product structure requirements, visible product and accessory structure must match the source reference, and product size/proportion must stay consistent across shots. If no product reference is available, skip product-accuracy review rather than inventing criteria.
- A failed image is unusable and must be regenerated; do not pass it as "mostly correct."
- For localized failures, use `gpt-image-2` edit mode through `aig-image-gen edit` before full regeneration when practical.
- Accepted regenerations or edits replace the original `shot-XX-*.png` stable filename. Temporary variant names, masks, and crops are only for inspection and should not remain as final delivery assets unless the user asks to keep variants.

## Sound Column Rules

- `音效配乐` only describes sounds that should actually be present in the shot.
- Keep `音效配乐` as one field, but write only the sound categories that serve the shot's main visual expression. Be concise: wide environment shots may only need `环境声`; dialogue shots should include `人声`; action or prop-focused shots may include `动作音效` or `道具声`; add `BGM` only when it supports the emotional rhythm.
- Do not write negative or reverse sound instructions such as "不加某声音", "不添加某音效", or "不额外添加产品声".
- If a sound should not appear, omit it. For low-noise products, use grounded environmental sound, action sound, character reaction, or normal conversation volume to imply quietness.

## HTML Requirements

`storyboard.html` must exist for every storyboard project.

No-image mode:

- Show the story core summary.
- Show project overview.
- Show the full storyboard content.
- Do not show image cards unless images have actually been generated.
- Show design analysis.

With-image mode:

- Keep the same storyboard content and analysis.
- Embed generated images using relative paths.
- Show local image filenames or paths.

Do not display image prompts unless the user explicitly requests them.
Do not leave temporary prompt files, dry-run text files, scratch `.txt` files, or assistant-only working notes in storyboard delivery folders. If image generation requires retry prompts or diagnostics, keep them outside the delivery folder or delete them before handoff. Prompt files are deliverables only when the user explicitly asks to save or export prompts.

Open local HTML preview files automatically without asking again once the environment has a reusable `Start-Process` approval. If that approval is not available yet, request it once with a reusable prefix rule. First-frame confirmation is conversational, not HTML-based.

`storyboard.md` uses per-shot blocks, not a wide Markdown table. Each shot block must use `镜头 N / 时长 / 景别 / 运镜 / 运镜逻辑 / 画面描述 / 文案旁白 / 音效配乐`; `时长` must be a cumulative range. Do not add `执行备注`, `首帧图方向`, or `首帧方向`.

## Output Paths

Use:

```text
outputs/YYYY-MM-DD-<project-name>/
```

Common files:

- `storyboard.md`
- `storyboard.html`
- `reference-character-3view-face.png`
- `reference-scene-concept.png`
- `shot-01-*.png`
- `shot-02-*.png`
- `shot-03-*.png`
- `shot-04-*.png`

Do not create `prompts/` by default.
Do not keep `.tmp.txt`, dry-run prompt dumps, or other scratch prompt files in dated output folders.

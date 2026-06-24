# TVC Short-Video Storyboard Workspace

This workspace contains project-local Codex skills and delivery files for product short-video storyboard work.

## Current Workflow

The storyboard workflow is split into three project skills:

- `short-video-storyboard`: writes the Chinese storyboard script and physical-world continuity analysis. It does not generate images directly.
- `storyboard-html-delivery`: creates or updates the final `storyboard.html`. HTML delivery is required whether first-frame images are generated or not.
- `storyboard-first-frame-images`: orchestrates first-frame continuity only after the user confirms they need images. It first creates a character reference sheet and a scene concept reference, then uses only those two images as inputs for every storyboard shot; it uses `aig-image-gen` for actual raster generation or editing.

The repository also includes the supporting project skill `aig-image-gen`, which provides the AIG/Joinin GPT Image CLI used by `storyboard-first-frame-images`. It reads credentials from each user's local Codex auth/config files; no API keys are stored in this repository.

## How To Use

1. Start with a product brief. If the user gives only a product name or an incomplete brief, automatically open `outputs/storyboard-brief-selector.html`, ask the user to send back the generated brief, and stop before writing any storyboard or HTML.
2. After the completed brief is available, ask for a storyboard. The script skill should produce `storyboard.md` and `storyboard.html`, and the script should also appear in the conversation.
3. Automatically open the generated `storyboard.html` for preview when possible.
4. Confirm first-frame generation directly in the conversation. The assistant should ask the user to choose: `需要生成首帧图`, `暂不生成首帧图`, or `先修改分镜再决定`.
5. If first frames are confirmed, run the first-frame skill. It calls `aig-image-gen` for the image files, performs a strict image-vs-storyboard review after the full set is generated, and then updates the same `storyboard.html`.

## Key Rules

- Do not auto-generate first-frame images during initial storyboard writing.
- Use `aig-image-gen` for confirmed first-frame image generation/editing.
- For first-frame images, every shot must use only `reference-character-3view-face.png` and `reference-scene-concept.png` as image inputs. Do not pass generated `shot-*.png` images back into later image-generation calls; preserve continuity through prompt text, storyboard causality, stable wardrobe, props, and scene layout.
- The scene concept reference must include every storyboard-critical product state and location state before shot generation, such as lights-off/lights-on, open/closed, dry/wet, installed/uninstalled, or before/after states.
- The scene concept reference is an environment map, not a cast image. Keep it free of people unless explicitly requested, and include wide/global, medium, and close-up views for the main recurring location or product-zone when practical.
- Accepted reference images are locked. If a reference needs refinement, generate a temporary candidate for inspection first and replace the stable `reference-*.png` only after user acceptance or an objective mismatch with explicit requirements.
- When the same object appears in two or more storyboard shots, include a compact object inventory in the character reference sheet prompt. Lock the recurring object's color, material, size, shape, worn/carried position, and character ownership/use.
- Character master/reference sheet prompts must include a hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
- After all first-frame images are generated, compare every image with its storyboard row. Excluding intentionally blurred faces, any visible mismatch in scene, time, space, people, wardrobe, props, product state/visibility, lighting, action, composition intent, or causality makes the image unusable and it must be regenerated.
- Visible text, label-like marks, UI-like fragments, or glyph artifacts do not by themselves fail the review. Treat them as a problem only when they contradict the storyboard, obscure required visual information, or conflict with explicit user requirements.
- When regenerating a shot, inspect a temporary candidate first. Once accepted, automatically replace the original stable `shot-XX-*.png` filename and keep `storyboard.html` pointing to that stable filename. Do not leave `-v2` or `-v3` variants as final delivery assets unless the user explicitly asks to keep variants.
- Always produce final HTML, even when images are not generated.
- Always include a short `故事核心` summary for storyboard deliveries and meaningful storyboard revisions. Include it in the conversation response, `storyboard.md`, and `storyboard.html` so the user can quickly judge the narrative before reading the full shot table.
- Auto-open the shared brief selector and generated storyboard HTML at their workflow stages. Do not use an HTML page for first-frame confirmation; handle that choice in the conversation.
- The shared brief selector has separate `平台` and `视频时长` fields. Duration buttons are `15秒`, `20秒`, `30秒`, and `60秒`, with `15秒` as the default.
- The shared brief selector is now social-video oriented: it collects opening hook, content structure, retention rhythm, transition technique, filming technique, and sound/packaging choices. Generated briefs should ask for creative recommendations first, then the storyboard.
- Storyboard shot durations are flexible. Assign duration by advertising function, information load, and platform rhythm; shots below `5秒` are allowed when the selling point remains legible.
- Preserve physical-world continuity: weather, time, space, people, wardrobe, props, product state, lighting, and event causality must remain coherent.
- Do not add proof elements such as water droplets, rain, new props, or new locations unless they were established earlier, caused by the current action, or normal for the scene.
- In the `音效配乐` field, write only sounds that should actually be heard and that serve the shot's main visual expression. Keep it concise: wide shots may only need `环境声`; dialogue shots should include `人声`; action or prop-focused shots may include `动作音效` or `道具声`; add `BGM` only when it supports the emotional rhythm. Omit absent categories instead of writing reverse instructions like "不添加产品声".
- `storyboard.md` uses the per-shot block format from `outputs/2026-06-03-downlight-city-hero/storyboard.md` by default, not a wide Markdown table. Each shot uses these fields in order: `镜头 N`, `时长：`, `景别：`, `运镜：`, `运镜逻辑：`, `画面描述：`, `文案旁白：`, `音效配乐：`. `时长` must be cumulative ranges such as `0-2.5秒`, `2.5-5秒`, `5-8秒`, not standalone shot durations. Do not add `执行备注` or first-frame direction fields.
- The `文案旁白` content defaults to English narration or English character dialogue unless the user explicitly requests Chinese copy. Keep the Chinese storyboard fields and analysis, but put the spoken copy in English.
- For voiced lines, include the voice description in the same `文案旁白` field. Repeat the same narrator voice anchor across narrator shots, and keep each recurring character's dialogue voice consistent across shots.
- Do not write screen copy in `文案旁白` by default. Use narration or character dialogue only unless the user explicitly asks for on-screen text/subtitles.
- Keep image prompts internal unless the user explicitly asks to save or show them.
- Do not leave temporary prompt files, dry-run text files, scratch `.txt` files, or assistant-only working notes in dated `outputs/` delivery folders. Prompt files are saved only when the user explicitly asks to keep or export them.
- Short-video rhythm is mandatory: each shot must create a new advertising information gain within the first 0.5 seconds. Avoid slow process beats such as a character walking over, seeing someone, or gradually moving closer unless the selling-point change is already visible in the opening frame.
- Write trigger points and result moments instead of full action processes: need before trigger, product intervention, visible result, then product/scene memory. Character movement should serve the product proof, not become the story itself.
- Use editing jumps to compress real movement while preserving continuity of space, people, props, product, and lighting.

## Important Paths

```text
H:\TVC
├── .codex\skills\aig-image-gen\
├── .codex\skills\short-video-storyboard\
├── .codex\skills\storyboard-html-delivery\
├── .codex\skills\storyboard-first-frame-images\
├── outputs\storyboard-brief-selector.html
├── docs\storyboard-workflow.md
└── PROJECT_FLOW.md
```

For the detailed operating procedure, see `docs/storyboard-workflow.md` and `PROJECT_FLOW.md`.

Existing dated folders under `outputs/` are historical deliveries. They are useful as archives, but they are not the source of truth for current workflow rules.

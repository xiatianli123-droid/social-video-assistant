# Session Summaries

This file stores dated workflow summaries for version management. When a project or workflow summary is generated in conversation, append or update the relevant dated section here.

## 2026-06-24

### Storyboard Skill Format Hardening

- Project directory: `H:\TVC`.
- Key rule or asset changes:
  - Investigated why a collaborator's generated storyboard collapsed into a short summary table instead of the project-standard per-shot block format.
  - Found that the strict `故事核心` and per-shot block rules were present in `AGENTS.md`, `README.md`, and `docs/storyboard-workflow.md`, but were not hard enough inside the published `short-video-storyboard` skill itself.
  - Updated `.codex/skills/short-video-storyboard/SKILL.md` to require `故事核心`, forbid wide Markdown tables/four-column summary tables, enforce fixed shot-field order, require cumulative time ranges, and require fuller per-shot execution detail.
  - Updated `references/storyboard-template.md` with the same fixed-format guardrails and refreshed `agents/openai.yaml` so the default prompt explicitly invokes `$short-video-storyboard`.
  - Removed the outdated Chinese six-question intake block from `short-video-storyboard` and its template reference. Incomplete briefs now route only through `outputs/storyboard-brief-selector.html` unless the user explicitly asks to use defaults.
  - Split the detailed Hook review mechanism out of `SKILL.md` into `references/hook-review.md`; `SKILL.md` now only indexes the reference and requires each completed Hook review/rewrite to append a compact new case to that reference file.
  - Added maintenance rules to `references/hook-review.md`: organize once `新增案例库` exceeds 20 entries, keep only 3-5 representative cases per Hook problem type, promote repeated lessons into rules, and archive old history only when needed.
- Current output status: `short-video-storyboard` validates successfully with the skill creator `quick_validate.py` script in UTF-8 mode.
- Next required step: commit and push the skill hardening changes so collaborators receive the stricter format rules.

### Git Packaging And Skill Cleanup

- Project directory: `H:\TVC`.
- Key rule or asset changes:
  - Initialized the workspace as a Git repository on `main` and created the initial project commit.
  - Added a root `.gitignore` for local temporary files, caches, editor metadata, and environment secrets.
  - Migrated media assets (`*.png`, `*.jpg`, `*.mp4`, `*.mp3`, `*.wav`) to Git LFS before publishing so large storyboard assets upload reliably.
  - Removed `.codex/skills/seedance-video/` because video-generation work is no longer part of this project; the active workflow ends after storyboard, HTML delivery, and optional first-frame image generation/review.
  - Confirmed the project-local active skills remain `short-video-storyboard`, `storyboard-html-delivery`, and `storyboard-first-frame-images`.
  - Added project-local `aig-image-gen` support skill so first-frame generation has its required AIG/Joinin GPT Image CLI in the repository; runtime credentials still come from each user's local Codex auth/config.
- Current output status: public GitHub repository created and `main` pushed to `https://github.com/xiatianli123-droid/social-video-assistant.git`.
- Next required step: collaborators should clone the repository with Git LFS installed so media assets download correctly.

## 2026-06-23

### Social Video Brief Panel

- Project directory: `H:\TVC`.
- Key rule or asset changes:
  - Reworked `outputs/storyboard-brief-selector.html` from an operations-oriented intake form into a social-video creative brief panel.
  - The panel now keeps basic product information, core selling points, scene, platform, and duration, then focuses on six creative groups: 开头钩子, 内容结构, 留存节奏, 转场技巧, 拍摄技巧, and 声音与包装.
  - Generated briefs now ask for social creative recommendations first: content hook, retention rhythm, transition idea, and filming/editing suggestions before the storyboard.
  - Restyled the brief panel with a black/acid-green AI video platform look inspired by a dark inspiration-gallery screenshot: narrow top navigation, cinematic liquid KV banner, sharp neon-green category buttons, and green highlight feedback on selected/clicked buttons.
  - Updated `PROJECT_FLOW.md`, `README.md`, and `docs/storyboard-workflow.md` to describe the social-video brief flow.
- Current output status: shared brief panel and workflow docs are updated; historical storyboard deliveries were not changed.
- Next required step: use the new panel for incomplete social-video briefs and keep transition suggestions tied to type, shared visual anchor, and narrative purpose.

### Transition Logic Reference

- Project directory: `H:\TVC`.
- Key rule or asset changes:
  - Converted the user-provided dynamic-design transition reference into a Markdown rule document at `docs/transition-logic.md`.
  - Added a transition design reference to `AGENTS.md` and `docs/storyboard-workflow.md` for future seamless transitions and cutaways, pointing to the Markdown document rather than an image.
  - Future storyboard transitions should be selected by purpose and shared visual anchor: 遮挡转场, 动势匹配转场 / match cut, 前后承接转场, 无缝转场, or 空镜转场.
- Current output status: Markdown reference and linked workflow rules are in place.
- Next required step: when writing a storyboard transition, explicitly state the shared visual anchor and why the cut is legible.

### TK Solar String Lights First-Frame Workflow

- Project directory: `outputs/2026-06-23-tk-solar-string-lights/`.
- Key rule or asset changes:
  - Created a 15-second TikTok storyboard for TK solar outdoor string lights with a hook built around an old short string light reaching its end and splitting the patio into lit/dark zones.
  - Generated two continuity references and four stable first-frame images, then updated `storyboard.html` to reference the stable shot filenames.
  - Cleaned failed/candidate image artifacts from the project delivery folder, leaving only `storyboard.md`, `storyboard.html`, `reference-character-3view-face.png`, `reference-scene-concept.png`, and the four stable `shot-*.png` files.
  - Updated `storyboard-first-frame-images` and `docs/storyboard-workflow.md` so first-frame QA opens subagent visual review before delivery; product size/proportion consistency and product/accessory structure are checked only when explicit product references or structure requirements exist, while projects without product references are reviewed only for first-frame rule compliance, storyboard match, human deformation, pose/action correctness, scene continuity, lighting, and causality.
  - Clarified that temporary candidates, masks, crops, dry-run notes, and failed variants should not remain in delivery folders after final handoff unless the user asks to keep variants.
- Current output status: stable storyboard and four first-frame images remain in the project folder; failed candidates have been removed.
- Next required step: if the user wants the strict product QA findings fixed, locally edit or regenerate the affected stable shot images before final acceptance.

## 2026-06-15

### Summer Surf Vlog Storyboard

- Project directory: `outputs/2026-06-15-skydive-surf-speed/`.
- Key rule or asset changes:
  - Created a 30-second horizontal pure vlog storyboard around summer, beach arrival, surfing attempts, one successful ride, and sunset wrap-up.
  - Revised the middle section into one long 7-22 second sports sequence using first-person POV, water-level motion follow, low-altitude drone aerial, and return-to-POV wave exit.
  - Revised again to add a stronger cold-open hook with a first-person whitewater wipeout and a final drone pullback twist revealing the “epic” ride was actually a knee-high near-shore wave.
  - Revised again to remove the vlog/self-deprecating tone and shift the piece into a high-energy summer surf sports film focused on speed, heat, acceleration, wave-wall pressure, and a passionate drone-lift finish.
  - Revised the core sports sequence to include a giant wave: established a distant swell in shot 2, made the 6-22 second multi-camera sequence show the giant wave approaching and breaking behind the surfer, and carried the whitewater aftermath into the final drone-lift finish.
  - Revised the concept into a skydive-to-surf extreme sports film with a seamless cloud-whiteout-to-wave-foam transition, followed by the giant-wave surfing sequence.
  - Compressed the concept to a 20-second fast-cut version with a 0-2 second strong hook, a 5-8 second seamless cloud-to-wave transition, an 8-16 second giant-wave surf climax, and a 16-20 second drone-lift finish.
  - Revised the final 16-20 second shot into a twist ending: the extreme sports sequence is revealed as a designer's imagined/working creative film when a phone call interrupts with “图片怎么还没做好？”, then the designer puts down the phone and continues working from a sunset beach setup, ending on a back-view composition with sea, sand, and sunset.
  - Simplified the twist ending without changing timing: kept the 8-16 second surf climax intact and reduced the final 16-20 second shot to a clear action chain of wave exit, phone ring, one催图 line, phone down, and back-view working silhouette.
  - Removed the 20-second cap and revised the structure to about 26 seconds: shot 3 now contains the full seamless skydive-to-surf transition and complete surfing sequence from wave entry through giant-wave exit, shot 4 contains only the phone-call designer reveal, and shot 5 gives the sunset beach back-view ending more time to breathe.
  - Revised timing to about 23 seconds: shot 4 now bridges the surf climax into reality with the protagonist walking out of the water onto the beach before the phone rings, and shot 5 is a concise 21-23 second back-view sunset ending.
  - Used the required per-shot block format in `storyboard.md` with cumulative time ranges and fields `镜头 N / 时长 / 景别 / 运镜 / 运镜逻辑 / 画面描述 / 文案旁白 / 音效配乐`.
  - Added a compact `故事核心` to both Markdown and HTML.
  - Created a no-image `storyboard.html` delivery page; no first-frame images were generated.
- Current output status: `storyboard.md` and `storyboard.html` exist in the project folder.
- Next required step: wait for the user's confirmation choice: `需要生成首帧图 / 暂不生成首帧图 / 先修改分镜再决定`.

## 2026-06-12

### Downlight City Hero Storyboard Formatting

- Project directory: `outputs/2026-06-03-downlight-city-hero/`.
- Key rule or asset changes:
  - Reformatted `storyboard.md` from a wide Markdown shot table into per-shot text blocks matching the requested image-style layout.
  - Changed each shot's `时长` field from standalone duration to cumulative time ranges: `0-2.5秒`, `2.5-5秒`, `5-8秒`, `8-11.5秒`, and `11.5-15秒`.
  - User confirmed `outputs/2026-06-03-downlight-city-hero/storyboard.md` is the ongoing storyboard template: future `storyboard.md` files use per-shot blocks with cumulative time ranges and fields `镜头 N / 时长 / 景别 / 运镜 / 运镜逻辑 / 画面描述 / 文案旁白 / 音效配乐`.
  - Updated `AGENTS.md`, `PROJECT_FLOW.md`, `README.md`, and the local `short-video-storyboard` skill/template to document that format.
  - Story content, shot descriptions, narration lines, and sound design were not rewritten.
- Current output status: `outputs/2026-05-28-downlight-tvc/storyboard.md` was converted to the same per-shot block format with cumulative time ranges; its `storyboard.html` duration cells were updated to match.
- Next required step: use this per-shot block format and cumulative timing for future storyboard Markdown deliveries; keep HTML aligned with the script timing.

### Project-Wide Storyboard Format Cleanup

- Project directory: `H:\TVC`.
- Key rule or asset changes:
  - Audited project docs, shared brief selector, project skills, reusable references, historical `outputs/*/storyboard.md`, and `storyboard.html` files for old wide-table wording.
  - Converted historical storyboard Markdown files under `outputs/` from wide tables to per-shot blocks with cumulative time ranges.
  - Updated HTML delivery pages to use `文案旁白` and `音效配乐` labels, cumulative time ranges, split platform/time labels where found, and removed old `执行备注` / pending first-frame-direction placeholders.
  - Updated `docs/storyboard-workflow.md`, `outputs/storyboard-brief-selector.html`, `storyboard-html-delivery`, and `case-pool-party-fan-light.md` so future generated briefs and reference examples no longer reintroduce the old format.
- Current output status: `rg` checks no longer find old Markdown storyboard tables, standalone HTML duration cells, slash labels in delivery files, or pending first-frame-direction panel references outside explicit rule-prohibition text.
- Next required step: future storyboard work should use the block format directly; no further format migration is currently pending.

### Seedance Video Skill

- Project directory: `.codex/skills/seedance-video/`.
- Key rule or asset changes:
  - Added a project-local `seedance-video` skill for Volcengine Ark Seedance 2.0 video task creation, polling, troubleshooting, and result download.
  - Added `references/seedance-api.md` as the standalone authoritative API document and updated `SKILL.md` to require reading it before API work.
  - Added `scripts/seedance_task.py` to build payloads, create tasks, query/poll task IDs, and download output videos without hardcoding API keys.
  - Added automatic credential loading from `.env.local` or `ark_api_key.txt`, plus `.gitignore` and `.env.example` for one-time local setup.
- Current output status: skill folder validates successfully; helper script syntax check and dry-run payload generation passed.
- Next required step: none. On 2026-06-24 this project retired the Seedance workflow and removed `.codex/skills/seedance-video/`; keep this entry only as historical context.

## 2026-06-04

### Downlight City Hero

- Project directory: `outputs/2026-06-03-downlight-city-hero/`.
- Storyboard exists in `storyboard.md`; HTML exists in `storyboard.html`.
- Current rule changes captured in project docs:
  - Reference-only changes and partial shot-image progress must not update `storyboard.html`.
  - `storyboard.html` should be updated only after the full first-frame set is generated or regenerated and passes review.
  - Visible text, label-like marks, UI-like fragments, or glyph artifacts do not by themselves fail image review; treat them as issues only if they contradict the storyboard, obscure required information, or conflict with explicit user requirements.
  - Character master/reference sheet prompts must include the hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
- Reference assets:
  - `reference-scene-concept.png` was regenerated as a scene concept board covering city crisis, target high-rise window, dark interior, downlight/switch detail, lit interior, and warm-white light countering red light.
  - Previous scene reference is preserved as `reference-scene-concept-prev-20260603-1707.png`.
  - `reference-character-3view-face.png` was replaced with the user-approved candidate version.
  - Previous character reference is preserved as `reference-character-3view-face-prev-20260603-1630.png`.
- First-frame assets currently present:
  - `shot-01-city-destruction.png`
  - `shot-02-target-window.png`
  - `shot-03-switch-downlights.png`
  - `shot-04-light-clash.png`
  - `shot-05-product-memory.png`
- Next required step: perform strict image-vs-storyboard review for all five shot images before any final HTML update.

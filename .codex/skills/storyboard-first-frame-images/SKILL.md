---
name: storyboard-first-frame-images
description: Generate reference-guided sequential first-frame images for an already completed short-video storyboard after the user confirms they need first frames. Before shot images, create a character 3-view plus face-detail reference and a scene concept reference, then use only those two images as image inputs for every storyboard shot; never pass generated shot images as references. Use when the user says they need 首帧图, first-frame images, AIG-generated storyboard frames, 执行首帧图片 skill, or clearly confirms first-frame generation after a storyboard script already exists. Do not use for initial storyboard writing or HTML delivery.
---

# Storyboard First Frame Images

Generate first-frame images only after a storyboard script exists and the user has confirmed they need images. This skill owns visual continuity, reference image orchestration, and shot-image generation; it does not write the original script or own the final HTML page. Use `aig-image-gen` for all raster image generation or editing calls.

## Required Inputs

- Completed storyboard script with shot table and visual descriptions.
- Project output directory, default `outputs/YYYY-MM-DD-<project-name>/`.
- People, wardrobe, scene, time of day, lighting, product state, and props from the storyboard.
- Any brand, product, logo, packaging, or compliance constraints already captured in the storyboard.

If safe, infer missing visual details from the storyboard. Ask only when missing information would materially change the reference images or the shot images.

## Required Reference-First Workflow

Do not generate storyboard shot images directly. Always create and approve two continuity reference images first:

1. **Character reference sheet**
   - File name: `reference-character-3view-face.png`.
   - Content: one consistent character sheet with front view, 3/4 side view, rear or profile view, and a face-detail close-up.
   - Include stable wardrobe, hair, age range, body type, skin tone, accessories, and expression range from the storyboard.
   - Include a hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
   - If the storyboard has multiple recurring characters, include each recurring character in the sheet only when they must stay consistent across shots; otherwise prioritize the main character.
2. **Scene concept reference**
   - File name: `reference-scene-concept.png`.
   - Content: one clean concept view of the main location showing spatial layout, materials, furniture, hero product position, prop positions, time of day, lighting direction, and color system.
   - This is an empty environment reference by default: no people, no silhouettes, no faces, and no characters unless the user explicitly asks for people in the scene concept.
   - Include wide/global view, medium view, and close-up view for the main recurring location or product-zone when practical, so later shots can preserve spatial continuity across camera scales.
   - If the storyboard uses multiple product or location states, the scene concept must include all states required for continuity, such as lights-off/lights-on, open/closed, dry/wet, installed/uninstalled, or before/after states.
   - Do not make this a final storyboard shot. It is a continuity map for all later shots.
3. Inspect both references before shot generation:
   - Check person identity, wardrobe, facial consistency, space layout, product position, lighting logic, and color system.
   - If a reference is clearly wrong or missing an explicit required state, generate a temporary candidate for inspection before replacing the stable `reference-*.png` file.
   - Once the user accepts a reference image, treat it as locked. Do not overwrite it because of assistant-only preference or uncertainty; replace it only after user acceptance or an objective mismatch with explicit requirements.
   - Do not let a flawed reference become the base for all shot images.

## Shot Image Workflow

1. Read the storyboard and extract shot count, scene, product identity, people, time, lighting, color system, props, and causality.
2. Run the continuity gate:
   - Weather, time, space, people, wardrobe, props, product state, lighting, and event causality must remain coherent.
   - Every new visual element must have a source: established earlier, produced by current action, or normal for the scene.
   - Do not add a proof element that violates the physical world.
3. Generate `reference-character-3view-face.png`.
4. Generate `reference-scene-concept.png`.
   - Include every storyboard-critical product or scene state in this reference before shot generation.
   - Keep the scene concept people-free unless explicitly requested, and include wide/global, medium, and close-up views where practical.
   - If refining an accepted reference, generate a candidate first and do not overwrite the accepted stable file until it is approved.
5. Generate shot images in strict order: Shot 1 -> Shot 2 -> Shot 3 -> remaining shots.
6. For every shot image, use only the two reference images as image inputs: `reference-character-3view-face.png` and `reference-scene-concept.png`. Do not use any generated shot image as an image input for any later shot.
   - Character reference preserves identity, face, hair, wardrobe, body type, and recurring accessories.
   - Scene reference preserves spatial layout, furniture, materials, product placement, lighting direction, and color palette.
   - Shot-to-shot continuity must be handled in the prompt text and storyboard logic, not by passing earlier shot images as references.
7. Save final images directly in the project output directory with stable names such as `shot-01-*.png`.
8. After the completed shot set is generated, open subagent visual QA before delivery. If the task includes explicit product reference images or product structure requirements, assign a product-consistency QA pass that compares all final shot images against the product reference and against each other. If there is no explicit product reference, skip product QA and review only first-frame rule compliance, storyboard match, people, pose/action, scene continuity, lighting, and causality.
9. Default to not saving and not showing image prompts. Save or show prompts only when the user explicitly asks.
10. After every shot passes subagent QA and main-agent integration review, invoke or follow `storyboard-html-delivery` to update the same `storyboard.html` with image cards and paths.

## Prompting Rules

- Every reference and shot prompt must include the task, product identity, scene state, composition, lighting, continuity anchors, and negative constraints.
- Reference prompts must describe identity and layout neutrally; shot prompts must describe the first frame of the specific storyboard shot.
- Character master/reference sheet prompts must explicitly avoid Asian facial features for recurring human characters.
- Keep people consistent when people appear: same approximate identity, wardrobe, role, hair, accessories, and relationship to the product.
- Keep the product family consistent across all shots. If the product is hidden until a later shot, maintain its implied location in the scene reference.
- Keep time progression plausible. A dusk-to-night progression is allowed; sudden weather or location jumps are not.
- First frames for short-video ads must already be in action. Show the trigger point or result moment directly.
- The first 0.5 seconds of each generated frame should make the advertising function legible: pain point, core selling point, reaction proof, or product memory.
- Use editing logic to compress real movement. The next frame may jump to the result of an action as long as the physical world remains coherent.
- Avoid identity drift, changed wardrobe, changed room layout, changed product position, extra logos, impossible reflections, and new props that were not established or normal for the scene.

## AIG Usage Rules

- Use `aig-image-gen` for actual generation/editing.
- Run a dry-run first when composing command options, output paths, model parameters, or multi-image inputs.
- For shot images, prefer `edit` with repeated `--image` inputs:
  - `--image reference-character-3view-face.png`
  - `--image reference-scene-concept.png`
- Do not include any `shot-*.png` file as an image input.
- Do not pass `--quality` by habit. Use the AIG CLI defaults unless the user or project requires a specific quality.
- During long generation, check whether the target file has landed on disk and whether dimensions are readable; do not rely only on process stdout.

## Visual QA And Local Edit Rules

- Open subagent visual QA for the completed first-frame set before calling it complete. The subagent review must inspect the final stable `shot-*.png` files, not rejected candidates.
- Give the QA subagent the storyboard, available product reference images or product structure requirements, reference sheets, and all final shot images. Ask for pass/fail per shot and a concrete fix recommendation: acceptable, localized `gpt-image-2` edit, or full regeneration.
- Run product QA only when the task includes explicit product reference images or explicit product structure requirements. If no product reference is available, do not invent product-accuracy criteria; review the shot set only for first-frame rule compliance, storyboard match, human body and hands, pose/action correctness, scene continuity, lighting, and causality.
- When product QA is enabled, check two cross-shot gates:
  - Product size and proportion stay consistent across all storyboard images where the product appears. Perspective changes are allowed, but the same object must not randomly become a different scale, thickness, bulb size, remote size, panel size, or cable weight from shot to shot.
  - Product structure matches the user's reference image: every visible recurring component keeps the same shape, material, color, attachment logic, button layout, lamp socket, hook/clip, bulb, cable, solar panel, remote, packaging, and accessory relationship.
- The QA pass must also check human body and hands, pose/action correctness, scene continuity, lighting, and whether the first frame is already in the shot's starting event or result moment.
- The main agent integrates the subagent findings and performs a final sanity pass before accepting or editing any file. If subagents are unavailable, perform the same checks directly and say that subagent QA could not be used.
- When product QA is enabled, product and accessory accuracy is a hard gate. If the visible product contradicts the source reference or is inconsistent with the product scale/proportion in other shots, mark the image failed even when the scene and people look good.
- White guide lines, layout dividers, label-like marks, or small text artifacts do not fail by themselves. Fail them only when they obscure required visual information, contradict the storyboard/product, or violate an explicit user requirement.
- If a shot fails only in a localized area, use `gpt-image-2` edit through `aig-image-gen edit` for a local correction instead of regenerating the whole shot by default.
- Write edited attempts to temporary candidate filenames first, such as `candidate-shot-02-product-fix.png` or `shot-02-*-candidate.png`. Inspect candidates visually before replacing the stable `shot-XX-*.png` file.
- Replace the stable filename only after the candidate passes the same subagent QA and main-agent sanity pass. Keep `storyboard.html` pointed at the stable filename.
- Do not leave failed candidates, masks, crops, dry-run notes, or assistant-only scratch files in the delivery folder after final handoff unless the user explicitly asks to keep variants.

## Output Rules

- Save reference images and shot images under `outputs/YYYY-MM-DD-<project-name>/`.
- Use PNG unless the user requests another format.
- Report saved filenames and dimensions.
- Do not delete old images unless the user explicitly asks. If replacing a bad frame, generate a candidate first; after it passes visual QA, replace the original stable `shot-XX-*.png` filename instead of changing final HTML to a variant name.
- Keep image prompts internal unless explicitly requested.

## References

- Read `references/image-reference.md` when designing reference images, continuity prompts, or sequential image generation.
- Use `aig-image-gen` when making the actual image generation/editing calls.

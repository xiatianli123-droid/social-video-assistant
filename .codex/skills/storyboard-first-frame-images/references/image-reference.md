# First-Frame Reference Images And Sequential AIG Generation

## Goal

Generate visual references and storyboard first frames that help clients, production teams, editors, and AI video tools understand the starting frame of each shot while preserving character and scene continuity.

## Reference Image Layer

Before generating any storyboard shot image, create two continuity references.

### Character Reference Sheet

File: `reference-character-3view-face.png`

Use one image as a compact identity sheet:

- Front view.
- 3/4 side view.
- Rear or profile view.
- Face-detail close-up.

The sheet must lock:

- Age range, face shape, skin tone, hair color, hairstyle, body type, and expression baseline.
- A hard constraint that recurring human characters avoid Asian facial features and should not appear as Asian faces.
- Wardrobe color, fabric type, accessories, and footwear when visible in later shots.
- Any recurring object carried by the character, such as earrings, phone, remote, cup, or tool.

If the same object is mentioned in two or more storyboard shots, add a compact object inventory to the character reference sheet prompt. The inventory must name each recurring object and lock its visible traits, including color, material, size, shape, worn/carried position, and which character uses or carries it. Keep the inventory visual and practical.

Do not turn the character sheet into a storyboard moment. It is a neutral continuity reference, usually full-body or half-body plus face detail, with simple background.

### Scene Concept Reference

File: `reference-scene-concept.png`

Use one image as a continuity map for the main location:

- Establish the main room, outdoor area, commercial space, or other location.
- Show furniture placement, wall/floor materials, windows/doors, hero product position, key props, and likely camera-friendly zones.
- Establish time of day, lighting direction, practical light state, and color palette.
- Keep the scene plausible for all storyboard shots.

Do not make the scene concept a final shot frame. It is a neutral location reference that later shots reinterpret through different framing.

## Continuity Gate

Before each shot image, check:

- Scene: same space structure, furniture, prop positions, wall/floor materials, door/window direction.
- Product: same product appearance, installation position, orientation, and on/off state progression.
- People: same age range, face, hair, wardrobe, accessories, body type, role, expression progression, and action route.
- Lighting: same main light direction; brightness changes must follow the story.
- Color: same palette and photographic style.
- Time: same time period, or a clear and plausible progression.
- Causality: every new visual element must be established earlier, caused by the current action, or normal for the scene.

If a reference image fails the gate, regenerate the reference before generating shot images.

## Sequential Generation Flow

Do not use one batch generation for a continuous storyboard sequence.

1. Generate the character reference sheet and inspect it.
2. Generate the scene concept reference and inspect it.
3. Generate Shot 1 using the character reference and scene reference.
4. Generate every storyboard shot using only the character reference and scene reference as image inputs.
5. Do not include Shot 1, Shot 2, or any other generated `shot-*.png` as an image input for later shots.
6. Continue this two-reference pattern for all remaining shots.
7. If a shot drifts obviously, fix or regenerate that shot before continuing.

The character reference and scene reference are the only image-reference sources. Preserve shot-to-shot continuity through prompt text, storyboard causality, stable wardrobe, stable props, and the scene layout; do not pass earlier generated shot images back into the image model.

## Difference Rules

Continuity does not mean copying the same composition. Each first frame must have a different visual function:

- Shot 1: hook, pain point, need, or scene setup.
- Shot 2: product intervention, trigger moment, or core selling point.
- Shot 3: action progression, user reaction, coverage proof, or result moment.
- Final shot: product memory, evidence detail, emotional closure, or brand/product reveal.

Use the reference images to preserve identity, layout, product, materials, lighting direction, and palette. Do not reuse the same standing position, shot scale, wall close-up, or action unless the storyboard explicitly requires it.

## Internal Prompt Requirements

Reference prompts must include:

- `character reference sheet` or `scene concept reference` as the task.
- The storyboard title, product family, target market/style, and visual tone.
- The continuity anchors that must remain stable.
- Negative constraints: no logos unless provided, no distorted hands/faces.

Shot prompts must include:

- Current shot number and purpose: storyboard first-frame reference.
- Required reference inputs: character sheet and scene concept for every shot. Do not use generated shot images as reference inputs.
- What to preserve from references: identity, wardrobe, layout, materials, product location, lighting direction, color system.
- What may change: action, expression, shot scale, camera angle, lit state, prop interaction, foreground/background emphasis.
- The shot's advertising function: hook, product intervention, reaction proof, product memory, or emotional payoff.
- The short-video rhythm task: the first 0.5 seconds must already show the problem, trigger, result, or product memory.
- Avoid: changed face, changed wardrobe, changed room layout, changed product shape/position, extra logo, physically impossible proof.

## Practical AIG Pattern

Generate references with `generate`. Generate shot images with `edit` whenever possible, using multiple image inputs:

```bash
python <aig>/scripts/aig-image-gen.py edit \
  --image outputs/YYYY-MM-DD-project/reference-character-3view-face.png \
  --image outputs/YYYY-MM-DD-project/reference-scene-concept.png \
  --prompt "Shot N first frame..."
```

For every shot, use only the two reference images. Never add `--image outputs/YYYY-MM-DD-project/shot-*.png`.

During long generation calls, poll the intended output path. A file may be written before the command's final stdout is observed.

## Writing Requirements

- A first-frame prompt describes one starting frame, not a video prompt.
- The frame must already contain information gain; do not wait for the action to start.
- If people recur, define them first in the character sheet and reuse that description in every shot.
- If product state changes, state the exact status: unlit, just triggered, stable lighting, final reveal, packed, installed, etc.
- Do not turn camera movement into a full animation. The storyboard table owns camera movement; the image prompt owns the starting frame.

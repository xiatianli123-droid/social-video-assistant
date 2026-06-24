---
name: storyboard-html-delivery
description: Create or update final HTML delivery pages for short-video storyboard projects. Use when a storyboard must be delivered as HTML, when a storyboard script is complete, when first-frame images need to be embedded, or when updating storyboard.html after image generation. Always support both no-image and with-image modes.
---

# Storyboard HTML Delivery

Create the final single-file HTML delivery page for a storyboard project. This skill owns `storyboard.html` whether first-frame images exist or not.

## Modes

- No-image mode: create `storyboard.html` from the completed script. Do not show image cards when images have not been generated.
- With-image mode: update the same `storyboard.html` to embed generated first-frame images, local image paths, and concise image notes.

## Required Inputs

- Completed storyboard script or `storyboard.md`.
- Project output directory, default `outputs/YYYY-MM-DD-<project-name>/`.
- Optional generated images in the same project directory.
- Optional brand, packaging, logo, slogan, CTA, or compliance requirements only when they were explicitly captured in the storyboard.

## Workflow

1. Read the completed storyboard and identify project overview, per-shot blocks, design analysis, and output paths.
2. Detect whether usable first-frame images exist for the shots.
3. Create or update `storyboard.html` in the project output directory.
4. Keep HTML self-contained: inline CSS and JS only if needed; no external CDN.
5. Do not display image prompts. Only show human-facing storyboard content and local file paths.
6. Make the page usable in both states:
   - Before image generation, do not show image cards.
   - After image generation, show real image cards while keeping the same storyboard content and analysis.

## HTML Requirements

- Include project overview.
- Source `storyboard.md` uses per-shot blocks with fields `镜头 N / 时长 / 景别 / 运镜 / 运镜逻辑 / 画面描述 / 文案旁白 / 音效配乐`; `时长` values are cumulative ranges such as `0-2.5秒`.
- HTML may render those shot blocks as a readable table or card layout, but visible labels should use `文案旁白` and `音效配乐`, not the old slash labels.
- Do not add `执行备注`, `首帧图方向`, or `首帧方向`.
- Include a first-frame image section only when real generated first-frame images exist; use image cards with relative paths.
- Include design analysis focused on shot logic, motion logic, continuity, emotional curve, and brand memory.
- Use stable responsive dimensions for images and tables.
- Avoid nested cards, external dependencies, and visible implementation notes.

## Output Rules

- Always write the HTML as `storyboard.html` in the project output directory.
- If a source `storyboard.md` exists, do not overwrite it unless the user explicitly asks.
- If images are later generated, update the existing `storyboard.html` rather than creating a second HTML file.

## References

- Read `references/html-output.md` when building or updating the delivery page.

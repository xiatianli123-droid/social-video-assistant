---
name: aig-image-gen
description: "Generate, batch-generate, and edit raster images through the bundled AIG/Joinin GPT Image CLI. Use when the user asks Codex to create images, edit existing images, produce multiple image variants from prompts, run image-generation dry-runs, or create web-ready downscaled copies using Codex auth/config. Trigger for Chinese or English image tasks including: 生成图片, 生图, 出图, 画图, 做图, 编辑图片, 改图, 修图, 图片编辑, 批量出图, 批量生成图片, 批量生图, generate image, create image, edit image, batch image generation."
---

# AIG Image Gen

## Overview

Use `scripts/aig-image-gen.py` to generate or edit images with GPT Image models through the configured `model_providers.Joinin` endpoint. The script reads `OPENAI_API_KEY` from Codex `auth.json` and the provider `base_url` from Codex `config.toml`.

## Workflow

1. Select the operation:
   - `generate` for a new image from a prompt.
   - `edit` for modifying one or more input images, optionally with a PNG mask.
   - `generate-batch` for JSONL prompt batches with concurrency and retries.
2. Run `--dry-run` first when composing prompts, confirming output paths, or checking model options without making an API call.
3. Do not pass `--quality` unless the user explicitly asks for a quality level or the task requires overriding the default. Let the script default (`DEFAULT_QUALITY`) be the source of truth, and use `--dry-run` to verify the payload quality before generation.
4. Use explicit `--out` or `--out-dir` paths so generated files land in the current workspace or another user-visible location.
5. Add `--force` only when overwriting an existing output is intended.

## Commands

Run the script with the active Python launcher:

```bash
py <skill-dir>/scripts/aig-image-gen.py generate --prompt "..." --out output/imagegen/output.png
```

Generation example:

```bash
py <skill-dir>/scripts/aig-image-gen.py generate \
  --prompt "A clean product mockup of a translucent water bottle on a white table" \
  --style "studio product photography" \
  --out output/imagegen/bottle.png
```

Editing example:

```bash
py <skill-dir>/scripts/aig-image-gen.py edit \
  --image input/product.png \
  --prompt "Replace the background with a bright kitchen counter while preserving the product" \
  --out output/imagegen/product-edit.png
```

Batch JSONL example:

```jsonl
{"prompt":"Minimal app icon for a habit tracker","out":"habit-icon.png","style":"flat vector-like icon"}
{"prompt":"Editorial hero image of a compact writing desk","out":"desk-hero.png"}
```

```bash
py <skill-dir>/scripts/aig-image-gen.py generate-batch \
  --input prompts.jsonl \
  --out-dir output/imagegen/batch \
  --concurrency 5
```

## Options

- Use `--model gpt-image-2` by default.
- Use `--size 2048x2048` by default, or pass `auto` / `WIDTHxHEIGHT` to override. For `gpt-image-2`, width and height must be multiples of 16, max edge must be at most 3840px, total pixels must be between 655,360 and 8,294,400, and the aspect ratio must not exceed 3:1.
- Use `--quality low|medium|high|auto`; default is `medium`. Omit this option for normal generation so future default changes in the script take effect.
- Use `--output-format png|jpeg|webp`; default is `png`.
- Use `--background transparent` only with a model that supports it, such as `gpt-image-1.5`, and only with `png` or `webp` output.
- Use prompt augmentation fields such as `--scene`, `--subject`, `--style`, `--composition`, `--lighting`, `--palette`, `--materials`, `--text`, `--constraints`, and `--negative` to make prompts more structured. Add `--no-augment` to send the prompt unchanged.
- Use `--downscale-max-dim <pixels>` to write an additional web-sized copy beside each output; this requires Pillow.

## Dependencies And Config

- Require Python 3.11+ or `tomli` for TOML parsing.
- Require the `openai` Python package for API calls.
- Require Pillow only when using `--downscale-max-dim`.
- Override Codex paths with `CODEX_AUTH_PATH` and `CODEX_CONFIG_PATH` if the default `~/.codex/auth.json` and `~/.codex/config.toml` are not correct.
- Override slow request timeout with `AIG_REQUEST_TIMEOUT_SECONDS`.

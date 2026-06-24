---
name: seedance-video
description: Call Volcengine Ark Seedance 2.0 video generation APIs. Use when Codex needs to create, poll, troubleshoot, or script Seedance / Doubao Seedance video tasks, including text-to-video, image-reference video generation, video-reference generation, audio-reference generation, and multimodal payloads using `/api/v3/contents/generations/tasks`. After this skill loads, read `references/seedance-api.md` before doing API work.
---

# Seedance Video

Use Volcengine Ark Seedance 2.0 as an asynchronous video-generation service. This file is the skill index.

Mandatory first step: before composing payloads, explaining fields, creating tasks, polling tasks, troubleshooting responses, or editing the helper script, read `references/seedance-api.md` completely. Treat `references/seedance-api.md` as the authoritative local API document for this skill.

If another agent says it cannot find the API document, give it the explicit path:

```text
H:\TVC\.codex\skills\seedance-video\references\seedance-api.md
```

## Required Inputs

- API key from `--api-key`, `ARK_API_KEY`, `.env.local`, or `ark_api_key.txt`.
- Prompt text describing the video.
- Model ID, default `doubao-seedance-2-0-260128`.
- Publicly reachable reference asset URLs when using images, video, or audio references.
- Output ratio and duration when the user specifies them.

Ask for missing information only when it changes the request materially. Otherwise choose safe defaults: `16:9`, `5` seconds, `generate_audio=false`, `watermark=false`.

## Workflow

1. Read `references/seedance-api.md` completely.
2. Build a JSON payload directly or with `scripts/seedance_task.py`.
3. Submit the task with `create`.
4. Poll with `poll` when the user wants completion in the same turn.
5. Download the returned video URL immediately when delivery is needed; generated URLs may expire.
6. Save reusable payload examples outside delivery folders unless the user explicitly asks to keep them.

## Script Usage

Create from command-line flags:

```powershell
$env:ARK_API_KEY = "..."
python .codex\skills\seedance-video\scripts\seedance_task.py create `
  --text "First-person apple fruit tea ad..." `
  --image-url "https://example.com/start.jpg" `
  --image-url "https://example.com/end.jpg" `
  --video-url "https://example.com/reference.mp4" `
  --audio-url "https://example.com/music.mp3" `
  --generate-audio `
  --ratio "16:9" `
  --duration 11 `
  --wait `
  --download "outputs\seedance-result.mp4"
```

Create from a prepared payload file:

```powershell
python .codex\skills\seedance-video\scripts\seedance_task.py create --payload payload.json --wait
```

Query or poll an existing task:

```powershell
python .codex\skills\seedance-video\scripts\seedance_task.py get --task-id cgt-...
python .codex\skills\seedance-video\scripts\seedance_task.py poll --task-id cgt-... --download result.mp4
```

Use `--dry-run` to print the payload without sending the request.

## Credential Setup

For automatic local credential loading, create `.codex/skills/seedance-video/.env.local` with:

```text
ARK_API_KEY=ark-your-rotated-key
```

The helper script reads credentials in this order: `--api-key`, `ARK_API_KEY`, `.env.local`, then `ark_api_key.txt`. `.env.local` and `ark_api_key.txt` are ignored by `.gitignore`.

## Safety

- Never hardcode a bearer token in `SKILL.md`, scripts, docs, payload files, or conversation examples.
- If the user pastes a real key, tell them to rotate it before continuing with live calls.
- Require user approval before making a live generation call if it consumes paid quota and the user did not clearly ask to run it.
- Treat local file paths as invalid API asset URLs; upload or use public/TOS URLs before submitting.

## References

- `references/seedance-api.md`: endpoint shape, payload notes, response handling, example JSON, and script usage. Read this file first.
- `scripts/seedance_task.py`: helper for create/get/poll/download.

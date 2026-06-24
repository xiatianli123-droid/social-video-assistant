# Seedance 2.0 Ark API

This is the authoritative local API document for the `seedance-video` skill. Read it before composing payloads, explaining fields, creating tasks, polling tasks, troubleshooting responses, or editing the helper script.

## Safety

- Never hardcode a bearer token in `SKILL.md`, this API document, scripts, payload files, docs, or conversation examples.
- Use `ARK_API_KEY` or the local `.env.local` file as the default credential source.
- If the user pasted a real key in chat or a file, tell them to rotate it before live calls.
- Treat live create calls as paid/quota-consuming actions; run `--dry-run` first unless the user clearly asked for live generation.
- Use only public, API-reachable asset URLs for `image_url`, `video_url`, and `audio_url`; local file paths are not valid API inputs.

## Credential Auto Loading

The helper script reads credentials in this order:

1. `--api-key`
2. `ARK_API_KEY`
3. `.codex/skills/seedance-video/.env.local`
4. `.codex/skills/seedance-video/ark_api_key.txt`

Recommended one-time setup:

```powershell
Copy-Item .codex\skills\seedance-video\.env.example .codex\skills\seedance-video\.env.local
notepad .codex\skills\seedance-video\.env.local
```

Then put the rotated key in `.env.local`:

```text
ARK_API_KEY=ark-your-rotated-key
```

`.env.local` and `ark_api_key.txt` are ignored by the skill's `.gitignore`.

## Endpoints

Create task:

```http
POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
```

Get task:

```http
GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}
```

Headers:

```http
Content-Type: application/json
Authorization: Bearer <ARK_API_KEY>
```

## Common Payload

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    {
      "type": "text",
      "text": "Prompt text..."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/reference-start.jpg"
      },
      "role": "reference_image"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/reference-end.jpg"
      },
      "role": "reference_image"
    },
    {
      "type": "video_url",
      "video_url": {
        "url": "https://example.com/reference.mp4"
      },
      "role": "reference_video"
    },
    {
      "type": "audio_url",
      "audio_url": {
        "url": "https://example.com/reference.mp3"
      },
      "role": "reference_audio"
    }
  ],
  "generate_audio": true,
  "ratio": "16:9",
  "duration": 11,
  "watermark": false
}
```

## Field Guidance

- `model`: Use the enabled Seedance model ID for the user's Ark account. The current default in this skill is `doubao-seedance-2-0-260128`.
- `content`: Put the text prompt first, then reference assets in the order the prompt names them.
- `role`: Use `reference_image`, `reference_video`, or `reference_audio` for reference media.
- `generate_audio`: Set true when the requested video should include generated or referenced audio.
- `ratio`: Use the user-requested aspect ratio, commonly `16:9`, `9:16`, or `1:1`.
- `duration`: Use the requested seconds and keep it aligned with the prompt timing.
- `watermark`: Set false only when the user's account and usage rights permit watermark-free output.

## Response Handling

Create calls are asynchronous and return a task identifier. Query or poll the task endpoint until it succeeds or fails. Response schemas can vary by rollout, so scripts should look for these patterns:

- task id: `id`, `task_id`, or `data.id`
- status: `status`, `data.status`, or `task.status`
- output URL: `content.video_url`, `data.content.video_url`, `result.video_url`, or nested video/url fields
- error details: `error`, `message`, `data.error`, or `data.message`

Download the result video as soon as practical because generated asset URLs can be time-limited.

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

If `.env.local` is configured, omit `$env:ARK_API_KEY = "..."`.

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

## Troubleshooting

- `401` or `403`: Check the API key, account permissions, model availability, and regional endpoint.
- `400`: Validate JSON, content item shape, duration/ratio values, and public accessibility of reference URLs.
- Failed task status: Return the full redacted response to the user and identify the likely field or asset problem.
- No output URL after success: Inspect the full JSON before assuming failure; the URL may be nested under `data`, `result`, `output`, or `content`.

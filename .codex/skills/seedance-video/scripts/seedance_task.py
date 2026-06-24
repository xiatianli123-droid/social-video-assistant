#!/usr/bin/env python3
"""Create, query, poll, and download Volcengine Ark Seedance video tasks."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
DEFAULT_MODEL = "doubao-seedance-2-0-260128"
TERMINAL_SUCCESS = {"succeeded", "success", "completed", "done"}
TERMINAL_FAILURE = {"failed", "failure", "error", "cancelled", "canceled", "expired"}
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATHS = (
    SKILL_DIR / ".env.local",
    SKILL_DIR / "ark_api_key.txt",
)


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def read_key_file(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("ARK_API_KEY="):
            return stripped.split("=", 1)[1].strip().strip("\"'")
        if stripped.startswith("ark-"):
            return stripped
    return None


def configured_api_key(api_key: str | None, config: str | None = None) -> str | None:
    if api_key:
        return api_key
    if os.environ.get("ARK_API_KEY"):
        return os.environ["ARK_API_KEY"]
    paths = [Path(config)] if config else list(DEFAULT_CONFIG_PATHS)
    for path in paths:
        key = read_key_file(path)
        if key:
            return key
    return None


def auth_header(api_key: str | None, config: str | None = None) -> dict[str, str]:
    key = configured_api_key(api_key, config)
    if not key:
        searched = ", ".join(str(path) for path in DEFAULT_CONFIG_PATHS)
        raise SystemExit(
            "Missing API key. Set ARK_API_KEY, pass --api-key, or create one of: "
            f"{searched}"
        )
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }


def request_json(method: str, url: str, headers: dict[str, str], payload: Any | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc}") from exc

    if not body.strip():
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Response was not JSON: {body[:1000]}") from exc


def first_value(data: Any, names: set[str]) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in names and value not in (None, ""):
                return value
        for value in data.values():
            found = first_value(value, names)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for item in data:
            found = first_value(item, names)
            if found not in (None, ""):
                return found
    return None


def extract_task_id(data: dict[str, Any]) -> str | None:
    value = first_value(data, {"id", "task_id"})
    return str(value) if value is not None else None


def extract_status(data: dict[str, Any]) -> str | None:
    value = first_value(data, {"status", "state"})
    return str(value).lower() if value is not None else None


def extract_video_url(data: Any) -> str | None:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {"video_url", "url"} and isinstance(value, str) and value.startswith(("http://", "https://")):
                return value
            found = extract_video_url(value)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = extract_video_url(item)
            if found:
                return found
    return None


def content_item(kind: str, url: str, role: str) -> dict[str, Any]:
    key = f"{kind}_url"
    return {
        "type": key,
        key: {"url": url},
        "role": role,
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload:
        return load_json(args.payload)
    if not args.text:
        raise SystemExit("Pass --text or --payload.")

    content: list[dict[str, Any]] = [{"type": "text", "text": args.text}]
    for url in args.image_url or []:
        content.append(content_item("image", url, "reference_image"))
    for url in args.video_url or []:
        content.append(content_item("video", url, "reference_video"))
    for url in args.audio_url or []:
        content.append(content_item("audio", url, "reference_audio"))

    return {
        "model": args.model,
        "content": content,
        "generate_audio": bool(args.generate_audio),
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": bool(args.watermark),
    }


def download(url: str, output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as response:
        path.write_bytes(response.read())


def poll_task(task_id: str, args: argparse.Namespace) -> dict[str, Any]:
    headers = auth_header(args.api_key, args.config)
    deadline = time.time() + args.timeout
    last: dict[str, Any] = {}
    while time.time() < deadline:
        last = request_json("GET", f"{args.base_url}/{task_id}", headers)
        status = extract_status(last)
        print(dump_json(last), flush=True)
        if status in TERMINAL_SUCCESS:
            return last
        if status in TERMINAL_FAILURE:
            raise SystemExit(f"Task ended with status {status}.")
        time.sleep(args.interval)
    raise SystemExit(f"Timed out after {args.timeout} seconds waiting for task {task_id}.")


def cmd_create(args: argparse.Namespace) -> None:
    payload = build_payload(args)
    if args.dry_run:
        print(dump_json(payload))
        return

    headers = auth_header(args.api_key, args.config)
    response = request_json("POST", args.base_url, headers, payload)
    print(dump_json(response))
    task_id = extract_task_id(response)
    if args.wait:
        if not task_id:
            raise SystemExit("Could not find task id in create response.")
        final = poll_task(task_id, args)
        maybe_download(final, args.download)


def cmd_get(args: argparse.Namespace) -> None:
    headers = auth_header(args.api_key, args.config)
    response = request_json("GET", f"{args.base_url}/{args.task_id}", headers)
    print(dump_json(response))
    maybe_download(response, args.download)


def cmd_poll(args: argparse.Namespace) -> None:
    final = poll_task(args.task_id, args)
    maybe_download(final, args.download)


def maybe_download(response: dict[str, Any], output: str | None) -> None:
    if not output:
        return
    video_url = extract_video_url(response)
    if not video_url:
        raise SystemExit("No video URL found in response; cannot download.")
    download(video_url, output)
    print(f"Downloaded video to {output}")


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", help="Ark API key. Prefer ARK_API_KEY or local config.")
    common.add_argument("--config", help="Path to a file containing ARK_API_KEY=... or a raw ark-* key.")
    common.add_argument("--base-url", default=BASE_URL)
    common.add_argument("--interval", type=float, default=10)
    common.add_argument("--timeout", type=int, default=1800)
    common.add_argument("--download", help="Download output video to this path when available.")

    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", parents=[common], help="Create a Seedance video task.")
    create.add_argument("--payload", help="JSON payload file. Overrides builder flags.")
    create.add_argument("--text", help="Prompt text.")
    create.add_argument("--model", default=DEFAULT_MODEL)
    create.add_argument("--image-url", action="append")
    create.add_argument("--video-url", action="append")
    create.add_argument("--audio-url", action="append")
    create.add_argument("--ratio", default="16:9")
    create.add_argument("--duration", type=int, default=5)
    create.add_argument("--generate-audio", action="store_true")
    create.add_argument("--watermark", action="store_true")
    create.add_argument("--wait", action="store_true", help="Poll until the task finishes.")
    create.add_argument("--dry-run", action="store_true", help="Print payload without sending.")
    create.set_defaults(func=cmd_create)

    get = sub.add_parser("get", parents=[common], help="Get one task response.")
    get.add_argument("--task-id", required=True)
    get.set_defaults(func=cmd_get)

    poll = sub.add_parser("poll", parents=[common], help="Poll one task until terminal status.")
    poll.add_argument("--task-id", required=True)
    poll.set_defaults(func=cmd_poll)
    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

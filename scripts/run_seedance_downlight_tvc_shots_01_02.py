#!/usr/bin/env python3
"""Upload original downlight TVC references to TOS and create a Seedance task."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import tos


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "outputs" / "2026-05-28-downlight-tvc"
PYTHON = sys.executable

FILES = [
    ("character reference", PROJECT / "reference-character-3view-face.png"),
    ("scene reference", PROJECT / "reference-scene-concept.png"),
    ("shot 1 reference", PROJECT / "shot-01-earring-shadow.png"),
    ("shot 2 reference", PROJECT / "shot-02-light-finds-earring.png"),
]


def require_env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name) or default
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def upload_and_sign() -> list[str]:
    ak = require_env("VOLCENGINE_ACCESS_KEY")
    sk = require_env("VOLCENGINE_SECRET_KEY")
    bucket = require_env("TOS_BUCKET", "my-video-assets123")
    region = require_env("TOS_REGION", "cn-beijing")
    endpoint = require_env("TOS_ENDPOINT", "tos-cn-beijing.volces.com")
    prefix = os.environ.get("TOS_PREFIX", "seedance/downlight-tvc/2026-06-15/").strip("/")

    client = tos.TosClientV2(ak=ak, sk=sk, endpoint=endpoint, region=region)
    urls: list[str] = []
    for label, path in FILES:
        if not path.exists():
            raise SystemExit(f"Missing {label}: {path}")
        key = f"{prefix}/{path.name}"
        client.put_object_from_file(bucket=bucket, key=key, file_path=str(path))
        signed = client.pre_signed_url(
            tos.HttpMethodType.Http_Method_Get,
            bucket=bucket,
            key=key,
            expires=24 * 60 * 60,
        )
        url = getattr(signed, "signed_url", None) or getattr(signed, "url", None) or str(signed)
        if not url.startswith(("http://", "https://")):
            raise SystemExit(f"Could not derive signed URL for {label}: {type(signed).__name__}")
        print(f"Uploaded and signed {label}: {path.name}", flush=True)
        urls.append(url)
    return urls


def build_payload(urls: list[str]) -> dict:
    prompt = """Generate one continuous 5.5-second vertical cinematic home-lighting ad video using the four reference images in order: character design, scene concept, shot 1 frame, shot 2 frame.

Aspect and output: vertical 9:16, 720p, modern premium apartment lighting style, realistic, no subtitles, no visible brand logos.

Timeline:
0.0-2.5s: Low-angle close-up in a modern apartment living room at dusk. A tiny silver earring back has rolled beside the sofa leg, half swallowed by the sofa shadow on a warm wood floor. A woman's hand reaches in from frame edge; her fingertips stop just short of the earring. Keep the beige sofa texture, wood floor grain, coffee table leg hints, blue-gray evening window light, and intimate shallow-depth close-up from shot 1. Do not show the downlight fixture yet.
2.5-5.5s: Hard cut to the wall switch already being pressed by the woman's finger, then cut back to the floor. A clean, soft circular pool of downlight lands beside the sofa and reveals the tiny earring with a small silver glint. She stops searching and picks it up with two fingers; her body language shifts from tense to relieved, with a small relaxed smile. Keep the same living room, sofa, floor, window dusk color, white shirt and dark pants, and the light circle composition from shot 2. The downlight fixture itself remains off camera.

Continuity constraints: same woman, same apartment, same sofa, same wood floor, same small silver earring; dusk outside, warm interior light after the switch; elegant understated home-ad rhythm; camera movement should be smooth and readable, focused on the tiny object and the light finding it."""

    content = [{"type": "text", "text": prompt}]
    for url in urls:
        content.append({"type": "image_url", "image_url": {"url": url}, "role": "reference_image"})

    return {
        "model": "doubao-seedance-2-0-260128",
        "content": content,
        "generate_audio": False,
        "ratio": "9:16",
        "duration": 6,
        "resolution": "720p",
        "watermark": False,
    }


def main() -> None:
    if not os.environ.get("ARK_API_KEY"):
        user_key = os.environ.get("ARK_API_KEY") or os.getenv("ARK_API_KEY")
        if not user_key:
            # The helper script can still load .env.local / ark_api_key.txt.
            pass
    urls = upload_and_sign()
    payload = build_payload(urls)
    output = PROJECT / "seedance-shot-01-02.mp4"
    script = ROOT / ".codex" / "skills" / "seedance-video" / "scripts" / "seedance_task.py"

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        payload_path = Path(handle.name)
    try:
        cmd = [
            PYTHON,
            str(script),
            "create",
            "--payload",
            str(payload_path),
            "--wait",
            "--download",
            str(output),
        ]
        subprocess.run(cmd, cwd=str(ROOT), check=True)
    finally:
        try:
            payload_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()

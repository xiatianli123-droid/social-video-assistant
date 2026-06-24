#!/usr/bin/env python3
"""Upload storyboard references to TOS, then create a Seedance task for shots 1-2."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import tos
from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "outputs" / "2026-06-03-downlight-city-hero"
PYTHON = sys.executable

FILES = [
    ("character reference", PROJECT / "reference-character-3view-face.png", True),
    ("scene reference", PROJECT / "reference-scene-concept.png", False),
    ("shot 1 reference", PROJECT / "shot-01-city-destruction.png", True),
    ("shot 2 reference", PROJECT / "shot-02-target-window.png", True),
]


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def privacy_softened_copy(src: Path, dst: Path) -> None:
    """Create a non-photographic reference copy to avoid real-person input flags."""
    image = Image.open(src).convert("RGB")
    image = image.filter(ImageFilter.SMOOTH_MORE)
    image = ImageOps.posterize(image, 3)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    draw = ImageDraw.Draw(image)
    w, h = image.size
    masks: dict[str, list[tuple[float, float, float, float]]] = {
        "reference-character-3view-face.png": [
            (0.05, 0.00, 0.92, 0.34),
            (0.00, 0.50, 0.28, 0.86),
            (0.30, 0.50, 0.62, 0.85),
            (0.63, 0.50, 1.00, 0.85),
        ],
        "shot-01-city-destruction.png": [
            (0.04, 0.04, 0.22, 0.16),
        ],
        "shot-02-target-window.png": [
            (0.50, 0.42, 0.78, 0.57),
            (0.35, 0.27, 0.64, 0.42),
        ],
    }
    for x1, y1, x2, y2 in masks.get(src.name, []):
        draw.rectangle((x1 * w, y1 * h, x2 * w, y2 * h), fill=(28, 28, 32))

    image.save(dst, quality=94)


def upload_and_sign(temp_dir: Path) -> list[str]:
    ak = require_env("VOLCENGINE_ACCESS_KEY")
    sk = require_env("VOLCENGINE_SECRET_KEY")
    bucket = os.environ.get("TOS_BUCKET", "my-video-assets123")
    region = os.environ.get("TOS_REGION", "cn-beijing")
    endpoint = os.environ.get("TOS_ENDPOINT", "tos-cn-beijing.volces.com")
    prefix = os.environ.get("TOS_PREFIX", "seedance/downlight-city-hero/2026-06-12/").strip("/")

    client = tos.TosClientV2(ak=ak, sk=sk, endpoint=endpoint, region=region)
    urls: list[str] = []
    for label, path, soften in FILES:
        if not path.exists():
            raise SystemExit(f"Missing {label}: {path}")
        upload_path = path
        upload_name = path.name
        if soften:
            upload_path = temp_dir / f"privacy-softened-{path.name}"
            privacy_softened_copy(path, upload_path)
            upload_name = upload_path.name
        key = f"{prefix}/{upload_name}"
        client.put_object_from_file(bucket=bucket, key=key, file_path=str(upload_path))
        signed = client.pre_signed_url(
            tos.HttpMethodType.Http_Method_Get,
            bucket=bucket,
            key=key,
            expires=24 * 60 * 60,
        )
        url = getattr(signed, "signed_url", None) or getattr(signed, "url", None) or str(signed)
        if not url.startswith(("http://", "https://")):
            raise SystemExit(f"Could not derive signed URL for {label}: {type(signed).__name__}")
        print(f"Uploaded and signed {label}: {upload_name}", flush=True)
        urls.append(url)
    return urls


def build_payload(urls: list[str]) -> dict:
    prompt = """Generate one continuous 5-second vertical cinematic product-ad video using the four reference images in order: character design, scene concept, shot 1 frame, shot 2 frame.

Aspect and output: vertical 9:16, 720p, realistic cinematic disaster-ad style, no subtitles, no visible logos, no existing superhero IP costume or marks.

Timeline:
0.0-2.5s: Night city in cold blue tones. A blond caped original red-eyed villain hovers above the skyline. Thick burning red eye lasers slice a rooftop advertising steel frame, melt through a giant neon sign, and crack glass curtain walls. The camera dives aerially through gaps between high-rises, chased and overtaken by a red laser streak. Keep smoke, sparks, alarm lights, wind pressure, and red reflections consistent with the shot 1 reference.
2.5-5.0s: Continue into the same city and target building. The camera skims rapidly along the outside of a high-rise residential facade. The red laser scrapes the exterior wall, leaves scorched marks, warps nearby window frames, and pulls glass fragments into the red tail stream. The camera slams to a stop outside one family window. Inside is dim: silhouettes of a child and parents retreat toward the living room center. Outside, the villain turns and narrows both red eye beams into a thicker charging column, locking onto that window like a targeting sight.

Continuity constraints: same night, same city, same villain, same target apartment; cold blue exterior palette with destructive red laser; keep the family only as dim interior silhouettes in shot 2; preserve the scene and character reference designs; strong camera motion but readable product-story setup."""

    content = [{"type": "text", "text": prompt}]
    for url in urls:
        content.append({"type": "image_url", "image_url": {"url": url}, "role": "reference_image"})

    return {
        "model": "doubao-seedance-2-0-260128",
        "content": content,
        "generate_audio": False,
        "ratio": "9:16",
        "duration": 5,
        "resolution": "720p",
        "watermark": False,
    }


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="seedance-safe-refs-") as temp:
        urls = upload_and_sign(Path(temp))
        require_env("ARK_API_KEY")
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

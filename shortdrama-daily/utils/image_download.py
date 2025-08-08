from __future__ import annotations
import os
import time
import hashlib
from urllib.parse import urlparse
import requests

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def safe_filename(url: str, title: str | None = None) -> str:
    base = title or os.path.basename(urlparse(url).path) or "poster"
    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
    digest = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    return f"{base[:32]}_{digest}{ext}"


def download_image(url: str, out_dir: str, title: str | None = None, timeout: int = 10) -> str | None:
    os.makedirs(out_dir, exist_ok=True)
    filename = safe_filename(url, title)
    path = os.path.join(out_dir, filename)
    try:
        with requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        # 节流，避免触发风控
        time.sleep(0.8)
        return path
    except Exception:
        return None


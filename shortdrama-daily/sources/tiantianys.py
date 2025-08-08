from __future__ import annotations
"""
短剧天堂（tiantianys.com）非官方聚合站 轻量抓取：
- URL: http://www.tiantianys.com
- 仅作为补充信号源使用；解析尽量温和，避免大规模抓取
"""
from typing import Dict, Any, List
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
URLS = [
    "http://www.tiantianys.com",
]


def _parse_cards(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")
    items: List[Dict[str, Any]] = []
    # 弱选择：抓取首页前若干条带图卡片
    for a in soup.select("a")[:200]:
        img = a.find("img")
        if not img:
            continue
        poster = img.get("src") or img.get("data-src")
        title = (a.get("title") or img.get("alt") or a.get_text(strip=True) or "").strip()
        if poster and title and len(title) >= 2:
            items.append({
                "title": title,
                "platform": "短剧天堂(聚合)",
                "status": None,
                "poster": poster,
                "tags": [],
                "highlight": "",
            })
        if len(items) >= 12:
            break
    return items


def get_data() -> Dict[str, Any]:
    all_items: List[Dict[str, Any]] = []
    for url in URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            all_items.extend(_parse_cards(r.text))
            time.sleep(1.0)
        except Exception:
            continue
    return {"items": all_items, "upcoming": [], "_source": "public_pages"}


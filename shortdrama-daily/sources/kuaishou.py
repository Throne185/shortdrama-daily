from __future__ import annotations
"""
快手小剧场（H5入口）占位抓取：
- URL: https://kuaishou.com/short-drama
- 说明：页面多为动态渲染；此为轻量解析，若失败则返回空
"""
from typing import Dict, Any, List
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
URLS = [
    "https://kuaishou.com/short-drama",
]


def _parse_cards(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")
    items: List[Dict[str, Any]] = []
    # 尝试抓取包含图片和标题的卡片元素（弱选择）
    for a in soup.select("a")[:200]:
        img = a.find("img")
        if not img:
            continue
        poster = img.get("src") or img.get("data-src")
        title = (a.get_text(strip=True) or img.get("alt") or "").strip()
        # 过滤明显为空或导航
        if poster and title and len(title) >= 2:
            items.append({
                "title": title,
                "platform": "快手小剧场",
                "status": None,
                "poster": poster,
                "tags": [],
                "highlight": "",
            })
        if len(items) >= 10:
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


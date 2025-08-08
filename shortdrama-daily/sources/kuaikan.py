from __future__ import annotations
"""
点众科技·快看短剧（官网）占位抓取：
- URL: https://www.kuaikan.tv
- 说明：页面可能为动态渲染；此为轻量解析，若失败则返回空
"""
from typing import Dict, Any, List
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
URLS = [
    "https://www.kuaikan.tv",
]


def _parse_cards(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")
    items: List[Dict[str, Any]] = []
    # 尝试从带图的链接中抽取少量基础信息
    for a in soup.select("a")[:200]:
        img = a.find("img")
        if not img:
            continue
        poster = img.get("src") or img.get("data-src")
        title = (a.get("title") or img.get("alt") or "").strip()
        if poster and title:
            items.append({
                "title": title,
                "platform": "快看短剧",
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


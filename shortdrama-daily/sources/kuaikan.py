from __future__ import annotations
"""
点众科技·快看短剧（官网）抓取：Playwright 优先，失败回退 requests
- URL: https://www.kuaikan.tv
"""
from typing import Dict, Any, List
import time
import asyncio
import requests
from bs4 import BeautifulSoup

from .common_playwright import browser_context

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
URLS = [
    "https://www.kuaikan.tv",
]


def _parse_cards(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")
    items: List[Dict[str, Any]] = []
    # 经验性选择：卡片常见在带图链接中
    for a in soup.select("a")[:300]:
        img = a.find("img")
        if not img:
            continue
        poster = img.get("src") or img.get("data-src")
        title = (a.get("title") or img.get("alt") or img.get("aria-label") or a.get_text(strip=True) or "").strip()
        if not (poster and title and len(title) >= 2):
            continue
        # 去除导航/无关链接（简单过滤）
        if any(x in title for x in ("登录", "注册", "帮助", "下载")):
            continue
        items.append({
            "title": title,
            "platform": "快看短剧",
            "status": None,
            "poster": poster,
            "tags": [],
            "highlight": "",
        })
        if len(items) >= 16:
            break
    return items


async def _fetch_playwright(url: str) -> List[Dict[str, Any]]:
    async with browser_context() as ctx:
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(1800)
        html = await page.content()
        return _parse_cards(html)


def get_data() -> Dict[str, Any]:
    # Playwright 优先
    try:
        tasks = [_fetch_playwright(u) for u in URLS]
        results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        items = [it for sub in results for it in sub]
        if items:
            return {"items": items, "upcoming": [], "_source": "public_pages"}
    except Exception:
        pass
    # 回退 requests
    all_items: List[Dict[str, Any]] = []
    for url in URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            all_items.extend(_parse_cards(r.text))
            time.sleep(1.0)
        except Exception:
            continue
    return {"items": all_items, "upcoming": [], "_source": "public_pages" if all_items else "empty"}


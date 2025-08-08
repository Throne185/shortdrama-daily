from __future__ import annotations
"""
腾讯视频短剧公开页抓取（Playwright 优先）
- 先尝试用 Playwright 渲染频道页；失败则返回空，由上层聚合器回退
- 若聚合器无可用来源，再由上层回退到 sample
"""

import json
import asyncio
from typing import List, Dict, Any
from bs4 import BeautifulSoup

from .common_playwright import browser_context

# 公开列表页（占位，需要根据实际DOM完善）
TENCENT_SHORT_DRAMA_URLS = [
    "https://v.qq.com/channel/short_drama",
]


async def _fetch_page(url: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    async with browser_context() as ctx:
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        # 适度等待动态渲染
        await page.wait_for_timeout(1500)
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        # TODO: 根据真实DOM结构实现选择器
        # 示例（占位）：
        # for card in soup.select(".drama-card"):
        #     title = card.select_one(".title").get_text(strip=True)
        #     poster = card.select_one("img")["src"]
        #     items.append({"title": title, "platform": "腾讯视频", "poster": poster, "tags": [], "highlight": ""})
        return items


def get_data() -> Dict[str, Any]:
    try:
        tasks = [_fetch_page(u) for u in TENCENT_SHORT_DRAMA_URLS]
        results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        items = [it for sub in results for it in sub]
        return {"items": items, "upcoming": [], "_source": "public_pages" if items else "empty"}
    except Exception:
        return {"items": [], "upcoming": [], "_source": "empty"}


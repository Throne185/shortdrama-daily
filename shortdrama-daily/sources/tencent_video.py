from __future__ import annotations
"""
腾讯视频短剧公开页抓取（占位版）
- 仅示例：保留 URL 与选择器占位，方便后续完善
- 若抓取失败则回退到示例数据
"""

import json
import time
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

# 公开列表页（示例/占位）— 需人工确认
TENCENT_SHORT_DRAMA_URLS = [
    # TODO: 替换为腾讯视频短剧/竖短剧频道页的实际 URL
    # "https://v.qq.com/channel/shortdrama"  # 占位
]


def fetch_list() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for url in TENCENT_SHORT_DRAMA_URLS:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            # TODO: 根据真实 DOM 结构编写解析逻辑
            # 示例：for card in soup.select(".drama-card"):
            #   title = card.select_one(".title").get_text(strip=True)
            #   poster = card.select_one("img")["src"]
            #   items.append({"title": title, "poster": poster, ...})
            time.sleep(1.2)
        except Exception:
            continue
    return items


def fallback_sample() -> Dict[str, Any]:
    with open("shortdrama-daily/data/sample_items.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # 标记来源为 sample，便于上层写入正确的 latest.json
        data["_source"] = "sample"
        return data


def get_data() -> Dict[str, Any]:
    items = fetch_list()
    if not items:
        return fallback_sample()
    return {"items": items, "upcoming": [], "_source": "public_pages"}


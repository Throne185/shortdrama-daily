from __future__ import annotations
"""
聚合多平台公开页数据：腾讯视频 / 爱奇艺 / 优酷 / 芒果TV
- 设计为“可插拔”，后续可加入红果/河马剧场（若有公开H5页或开放接口）
- 若所有来源都为空，则由上层回退到 sample
"""
from typing import Dict, Any, List


def _safe_get(module_name: str) -> Dict[str, Any]:
    try:
        # 直接从顶层 sources 包导入子模块
        mod = __import__(f"sources.{module_name}", fromlist=["get_data"])  # type: ignore
        return mod.get_data()
    except Exception:
        return {"items": [], "upcoming": []}


def _dedupe_by_title(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result: List[Dict[str, Any]] = []
    for it in items:
        title = (it.get("title") or "").strip().lower()
        if not title:
            continue
        if title in seen:
            continue
        seen.add(title)
        result.append(it)
    return result


def gather_data() -> Dict[str, Any]:
    sources = [
        "tencent_video",
        "iqiyi",
        "youku",
        "mgtv",
        # 预留：红果/河马（若后续发现可合规的公开H5页）
        # "hongguo",
        # "hema",
    ]
    all_items: List[Dict[str, Any]] = []
    all_upcoming: List[Dict[str, Any]] = []

    for s in sources:
        data = _safe_get(s)
        items = data.get("items", [])
        upcoming = data.get("upcoming", [])
        if items:
            all_items.extend(items)
        if upcoming:
            all_upcoming.extend(upcoming)

    all_items = _dedupe_by_title(all_items)

    if not all_items and not all_upcoming:
        return {"items": [], "upcoming": [], "_source": "empty"}
    return {"items": all_items, "upcoming": all_upcoming, "_source": "public_pages"}


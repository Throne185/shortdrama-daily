from __future__ import annotations
"""
爱奇艺短剧公开页抓取（占位版）
- 当前未确定稳定的公开频道页 URL/选择器；先返回空，保持可插拔结构
"""
from typing import Dict, Any

def get_data() -> Dict[str, Any]:
    return {"items": [], "upcoming": [], "_source": "public_pages"}


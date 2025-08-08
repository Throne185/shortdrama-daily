from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel


class Comment(BaseModel):
    content: str
    source: str


class Item(BaseModel):
    title: str
    platform: str
    status: str | None = None
    poster: str | None = None
    poster_local: str | None = None
    tags: List[str] = []
    highlight: str = ""
    comment: Comment | None = None


class Upcoming(BaseModel):
    title: str
    platform: str
    date: str
    points: str


def normalize_items(raw_items: List[Dict[str, Any]]) -> List[Item]:
    items: List[Item] = []
    for r in raw_items:
        try:
            items.append(Item(**r))
        except Exception:
            # 跳过非法条目
            continue
    return items


def normalize_upcoming(raw_upcoming: List[Dict[str, Any]]) -> List[Upcoming]:
    ups: List[Upcoming] = []
    for r in raw_upcoming:
        try:
            ups.append(Upcoming(**r))
        except Exception:
            continue
    return ups


from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncIterator
from playwright.async_api import async_playwright


@asynccontextmanager
async def browser_context() -> AsyncIterator:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 2000},
            locale="zh-CN",
        )
        try:
            yield context
        finally:
            await context.close()
            await browser.close()


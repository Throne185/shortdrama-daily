from __future__ import annotations
import os
import json
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from pipeline.normalize import normalize_items, normalize_upcoming
from pipeline.safety_filter import safe_text
from utils.image_download import download_image


def load_data(use_sample: bool) -> dict:
    if use_sample:
        with open("shortdrama-daily/data/sample_items.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # 聚合多来源公开页（占位，逐步完善）
    try:
        from sources.aggregator import gather_data
        return gather_data()
    except Exception:
        # 回退腾讯视频占位源
        from sources.tencent_video import get_data
        return get_data()


def ensure_posters(items: list[dict], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for it in items:
        poster = it.get("poster")
        if not poster:
            continue
        local = download_image(poster, out_dir, title=it.get("title"))
        if local:
            rel = os.path.relpath(local, start="dist")
            it["poster_local"] = rel.replace("\\", "/")


def render_html(ctx: dict, out_path: str) -> None:
    env = Environment(loader=FileSystemLoader("shortdrama-daily/content/templates"), autoescape=False)
    tpl = env.get_template("wechat_daily.html.j2")
    html = tpl.render(**ctx)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def write_status(dist_dir: str, status: dict) -> None:
    os.makedirs(dist_dir, exist_ok=True)
    latest_path = os.path.join(dist_dir, "latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-sample", action="store_true", help="使用示例数据渲染")
    args = parser.parse_args()

    data = load_data(use_sample=args.use_sample)

    # 归一化
    items = normalize_items(data.get("items", []))
    upcoming = normalize_upcoming(data.get("upcoming", []))

    # 来源标记
    source_flag = data.get("_source", "sample" if args.use_sample else "public_pages")

    # 敏感词过滤
    for it in items:
        it.highlight = safe_text(it.highlight)
        if it.comment:
            it.comment.content = safe_text(it.comment.content)
    for up in upcoming:
        up.points = safe_text(up.points)

    # 下载海报
    out_posters_dir = os.path.join("dist", "posters")
    items_dicts = [it.model_dump() for it in items]
    ensure_posters(items_dicts, out_posters_dir)

    # 生成上下文
    today = datetime.now().strftime("%Y-%m-%d")
    title = f"今天这几部短剧，狠到我通勤路上都不敢快进"
    hook = "反转比早高峰还猛，三站路看完一季不是梦。"
    verdict = "喜欢快节奏与反转的朋友可以冲；介意甜宠/土味的可择优挑选。"

    ctx = {
        "title": title,
        "date": today,
        "hook": hook,
        "items": items_dicts,
        "upcoming": [up.model_dump() for up in upcoming],
        "verdict": verdict,
    }

    dist_dir = "dist"
    out_path = os.path.join(dist_dir, f"{today}_wechat.html")
    render_html(ctx, out_path)

    # 写入状态清单
    status = {
        "date": today,
        "output_html": os.path.basename(out_path),
        "item_count": len(items_dicts),
        "upcoming_count": len(ctx["upcoming"]),
        "data_source": source_flag,
    }
    write_status(dist_dir, status)

    print(f"已生成：{out_path}")


if __name__ == "__main__":
    main()


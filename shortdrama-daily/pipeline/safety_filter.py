BLOCKLIST = [
    # 基础风险词（可扩充）
    "政变", "造反", "恐怖袭击", "分裂国家",
    "黄色", "情色", "低俗", "擦边",
    "迷信", "巫术", "算命",
]


def safe_text(text: str) -> str:
    t = text or ""
    for w in BLOCKLIST:
        if w in t:
            t = t.replace(w, "*")
    return t


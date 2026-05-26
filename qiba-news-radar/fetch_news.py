from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import yaml


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
SOURCES_FILE = ROOT / "sources.yml"


def load_sources() -> list[dict]:
    with SOURCES_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    return config.get("sources", [])


def parse_time(entry: dict) -> str:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return ""
    return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()


def fetch_items() -> list[dict]:
    items: list[dict] = []
    for source in load_sources():
        feed = feedparser.parse(source["url"])
        for entry in feed.entries[:20]:
            items.append(
                {
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", "").strip(),
                    "source": source["name"],
                    "published_at": parse_time(entry),
                    "summary": entry.get("summary", "").strip(),
                    "source_category": source.get("category", ""),
                }
            )
    return items


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output = DATA_DIR / f"{today}.raw.json"
    output.write_text(
        json.dumps(fetch_items(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved raw news to {output}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import (  # noqa: E402
    build_qiba_pitch,
    build_story_angle,
    build_zh_summary,
    calculate_priority_score,
    load_keyword_rules,
    normalize_qiba_pitch,
    recommendation_level,
    select_top_picks,
    tag_item,
)


SAMPLE = {
    "title": "Introducing ChatGPT Futures: Class of 2026",
    "summary": (
        "OpenAI introduces 26 students and young builders using AI to solve "
        "real-world problems across astronomy, healthcare, education, language "
        "preservation, disaster response, and social impact. Each receives a "
        "$10,000 grant and access to OpenAI frontier models."
    ),
    "source": "openai.com",
    "link": "https://openai.com/index/introducing-chatgpt-futures-class-of-2026/",
    "published_at": "2026-05-06T00:00:00+00:00",
    "source_category": "ai",
}

EXPECTED_TAGS = {"AI教育", "学生Builder", "未来学习", "项目制学习"}
EXPECTED_PITCH_PHRASES = [
    "AI时代好学生画像",
    "真实问题",
    "项目制学习",
]


def contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def main() -> int:
    rules = load_keyword_rules()
    tags, directions = tag_item(SAMPLE, rules)
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    priority_score = calculate_priority_score(SAMPLE, tags, now)
    zh_summary = build_zh_summary(SAMPLE, tags)
    story_angle = build_story_angle(SAMPLE, tags)
    qiba_pitch = normalize_qiba_pitch(build_qiba_pitch(SAMPLE, tags, priority_score))

    enriched = {
        **SAMPLE,
        "tags": tags,
        "directions": directions,
        "zh_summary": zh_summary,
        "story_angle": story_angle,
        "qiba_pitch": qiba_pitch,
        "priority_score": priority_score,
        "recommendation_level": recommendation_level(priority_score),
        "is_duplicate": False,
    }

    top_picks = select_top_picks([enriched])
    output = {
        "sample": {
            "title": SAMPLE["title"],
            "source": SAMPLE["source"],
            "link": SAMPLE["link"],
            "published_at": SAMPLE["published_at"],
        },
        "current_result": {
            "tags": tags,
            "directions": directions,
            "priority_score": priority_score,
            "recommendation_level": enriched["recommendation_level"],
            "zh_summary": zh_summary,
            "story_angle": story_angle,
            "qiba_pitch": qiba_pitch,
            "selected_when_alone": bool(top_picks and top_picks[0]["link"] == SAMPLE["link"]),
        },
        "diagnostics": {
            "not_filtered": not enriched.get("is_duplicate", False),
            "enters_candidate_pool": priority_score > 0,
            "recognized_ai_student_profile": contains_any(
                " ".join(tags + directions + [story_angle, qiba_pitch]),
                ["AI时代学生画像", "AI时代好学生画像", "学生Builder", "项目制学习", "未来学习"],
            ),
            "expected_tags_present": sorted(EXPECTED_TAGS & set(tags)),
            "expected_tags_missing": sorted(EXPECTED_TAGS - set(tags)),
            "qiba_writability_high": priority_score >= 65,
            "pitch_mentions_expected_angle": contains_any(qiba_pitch, EXPECTED_PITCH_PHRASES),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    failed = [
        name
        for name, passed in output["diagnostics"].items()
        if isinstance(passed, bool) and not passed
    ]
    if output["diagnostics"]["expected_tags_missing"]:
        failed.append("expected_tags_missing")

    if failed:
        print("\nDIAGNOSIS: FAIL")
        print("Blocked checks: " + ", ".join(failed))
        return 1

    print("\nDIAGNOSIS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

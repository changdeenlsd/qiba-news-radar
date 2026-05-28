from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import (  # noqa: E402
    build_resource_item,
    item_text,
    load_keyword_rules,
    select_daily_resources,
    select_top_picks,
    tag_item,
)


def make_item(title: str, summary: str, source: str = "Google AI Blog", published_at: str | None = None) -> dict:
    return {
        "title": title,
        "summary": summary,
        "source": source,
        "link": "https://example.com/" + title.lower().replace(" ", "-"),
        "published_at": published_at or datetime.now(timezone.utc).isoformat(),
        "source_category": "education",
    }


def enrich(item: dict, rules: dict) -> dict:
    tags, directions = tag_item(item, rules)
    return {
        **item,
        "tags": tags,
        "directions": directions,
        "is_duplicate": False,
    }


def assert_resource(item: dict, expected: dict) -> dict:
    resource = build_resource_item(item)
    selected = select_daily_resources([item])
    assert selected, f"Expected resource to be selected: {resource}"
    for key, value in expected.items():
        if isinstance(value, set):
            assert resource[key] in value, f"{key}={resource[key]!r}, expected one of {value!r}"
        else:
            assert resource[key] == value, f"{key}={resource[key]!r}, expected {value!r}"
    assert resource["score"] >= 65, resource
    return resource


def assert_not_resource(item: dict) -> dict:
    resource = build_resource_item(item)
    selected = select_daily_resources([item])
    assert not selected, f"Expected resource to be rejected: {resource}"
    return resource


def top_pick_item(title: str, source_category: str, score: int, tags: list[str] | None = None, summary: str = "") -> dict:
    return {
        "title": title,
        "summary": summary,
        "source": title,
        "source_category": source_category,
        "link": "https://example.com/top/" + title.lower().replace(" ", "-"),
        "published_at": datetime.now(timezone.utc).isoformat(),
        "tags": tags or [],
        "qiba_pitch": "适合放入资料库，暂不建议单独成文。",
        "priority_score": score,
        "is_duplicate": False,
    }


def main() -> int:
    rules = load_keyword_rules()
    samples = {
        "google_ai_quests": enrich(
            make_item(
                "Google AI Quests",
                "Google offers an interactive AI literacy game for students aged 11-14, helping them learn how artificial intelligence can solve real-world problems.",
                "Google for Education Blog",
            ),
            rules,
        ),
        "mit_mathnet": enrich(
            make_item(
                "MIT Mathnet",
                "MIT Mathnet provides math challenge problems and mathematical resources for students interested in problem solving and olympiad-style mathematics.",
                "MIT News",
            ),
            rules,
        ),
        "english_reading": enrich(
            make_item(
                "English reading resource for Chinese students",
                "A free English reading resource offers graded reading materials, vocabulary practice and worksheets for ESL/EFL students.",
                "EdSurge",
            ),
            rules,
        ),
        "enterprise_tool": enrich(
            make_item(
                "AI enterprise productivity tool",
                "A company launches an AI productivity platform for enterprise workflow automation.",
                "TechCrunch AI",
            ),
            rules,
        ),
        "commercial_bootcamp": enrich(
            make_item(
                "Commercial tutoring bootcamp",
                "A tutoring company launches a limited-time paid math olympiad bootcamp and asks parents to sign up for a consultation.",
                "EdSurge",
            ),
            rules,
        ),
        "old_generic": enrich(
            make_item(
                "Old generic resource",
                "A classic learning website last updated many years ago with no recent discussion or new content.",
                "EdSurge",
                "2018-01-01T00:00:00+00:00",
            ),
            rules,
        ),
    }

    results = {
        "positive": [
            assert_resource(
                samples["google_ai_quests"],
                {"subject": "AI认知", "region": "英文世界", "resource_type": "互动游戏"},
            ),
            assert_resource(
                samples["mit_mathnet"],
                {"subject": "数学学习", "region": "英文世界", "resource_type": {"题库", "竞赛资源"}},
            ),
            assert_resource(
                samples["english_reading"],
                {"subject": "英语学习", "resource_type": {"阅读材料", "练习册"}},
            ),
        ],
        "negative": [
            assert_not_resource(samples["enterprise_tool"]),
            assert_not_resource(samples["commercial_bootcamp"]),
            assert_not_resource(samples["old_generic"]),
        ],
        "diagnostics": {
            key: {
                "tags": value["tags"],
                "text": item_text(value, value["tags"])[:180],
            }
            for key, value in samples.items()
        },
    }

    learning_resource_guard = top_pick_item(
        "Generic grammar listening tip",
        "learning_resource",
        60,
        [],
        "A short English grammar and listening tip for learners.",
    )
    strong_learning_resource = top_pick_item(
        "Students use AI literacy projects in school",
        "learning_resource",
        65,
        ["AI教育"],
        "Students build AI literacy projects in middle school.",
    )
    students_ai_only = top_pick_item(
        "Students with Disabilities Praise Assistive Technology Using AI",
        "learning_resource",
        42,
        ["AI", "教育研究"],
        "Students with disabilities praise assistive technology using AI.",
    )
    family_only = top_pick_item(
        "In Uganda, Cost of Attending School Keeps Children Home",
        "learning_resource",
        36,
        ["教育研究", "儿童与青少年", "家庭教育"],
        "The cost of attending school keeps children home.",
    )
    normal_news = top_pick_item("Regular education news", "ai_education", 50)
    top_picks = select_top_picks([learning_resource_guard, strong_learning_resource, students_ai_only, family_only, normal_news], limit=5)
    top_titles = {item["title"] for item in top_picks}
    assert "Generic grammar listening tip" not in top_titles, top_picks
    assert "Students use AI literacy projects in school" in top_titles, top_picks
    assert "Students with Disabilities Praise Assistive Technology Using AI" not in top_titles, top_picks
    assert "In Uganda, Cost of Attending School Keeps Children Home" not in top_titles, top_picks
    assert "Regular education news" in top_titles, top_picks
    results["learning_resource_top20_guard"] = {
        "blocked": "Generic grammar listening tip" not in top_titles,
        "strong_tag_allowed": "Students use AI literacy projects in school" in top_titles,
        "students_ai_only_blocked": "Students with Disabilities Praise Assistive Technology Using AI" not in top_titles,
        "family_only_blocked": "In Uganda, Cost of Attending School Keeps Children Home" not in top_titles,
        "non_learning_resource_unaffected": "Regular education news" in top_titles,
    }

    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("\nDIAGNOSIS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

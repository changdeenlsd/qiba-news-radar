from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import (  # noqa: E402
    calculate_priority_score,
    classify_topic_family,
    select_top_picks,
)


def make_item(title: str, summary: str, source: str = "OpenAI Blog", tags: list[str] | None = None, score: int | None = None) -> dict:
    item = {
        "title": title,
        "link": f"https://example.com/{abs(hash(title))}",
        "source": source,
        "source_category": "ai",
        "published_at": "2026-06-13T00:00:00+00:00",
        "summary": summary,
        "tags": tags or [],
        "qiba_pitch": "",
        "is_duplicate": False,
        "duplicate_reason": "",
        "first_seen_date": "",
    }
    if score is None:
        score = calculate_priority_score(item, item["tags"], datetime(2026, 6, 13, tzinfo=timezone.utc))
    item["priority_score"] = score
    item["topic_family"] = classify_topic_family(item)
    return item


def test_topic_family_classification_and_scoring():
    pure_ai = make_item(
        "OpenAI launches new enterprise model benchmark",
        "OpenAI announces a model upgrade, developer API benchmark, cloud infrastructure and enterprise productivity tools.",
        tags=["AI", "科技巨头", "OpenAI"],
    )
    ai_education = make_item(
        "Students use AI in classroom projects",
        "Teachers describe how students use AI for homework, assessment, classroom projects and real-world learning.",
        source="Google for Education Blog",
        tags=["AI", "教育研究", "AI教育", "未来学习"],
    )
    mental_health = make_item(
        "New report on teen mental health and exam stress",
        "A university research report explains youth mental health, test anxiety, academic pressure and parent-child communication.",
        source="The 74",
        tags=["青少年心理健康", "考试压力", "亲子关系"],
    )
    low_quality = make_item(
        "One simple trick cures teen anxiety",
        "A limited-time coaching package uses anxiety marketing and asks parents to sign up for a consultation.",
        source="EdSurge",
        tags=["焦虑", "课程销售"],
    )

    assert classify_topic_family(pure_ai) == "pure_ai_tech"
    assert classify_topic_family(ai_education) == "ai_education_student"
    assert classify_topic_family(mental_health) == "learning_psychology_family"
    assert low_quality["priority_score"] <= 45
    assert mental_health["priority_score"] > pure_ai["priority_score"]


def test_top20_soft_balance_keeps_ai_education_and_limits_pure_ai():
    sources = [
        "OpenAI Blog",
        "Google AI Blog",
        "Microsoft Education Blog",
        "Google for Education Blog",
        "MIT News",
        "Stanford HAI",
        "EdSurge",
        "The 74",
        "Inside Higher Ed",
        "Quanta Magazine",
        "MIT Technology Review",
        "Education Source A",
        "Education Source B",
        "Education Source C",
    ]
    pure_ai_items = [
        make_item(
            f"OpenAI enterprise model upgrade benchmark {index}",
            "OpenAI announces a model upgrade, benchmark, developer API, cloud infrastructure and enterprise partnership.",
            source=sources[index % len(sources)],
            tags=["AI", "科技巨头", "OpenAI"],
            score=70 - index,
        )
        for index in range(12)
    ]
    ai_education_items = [
        make_item(
            f"AI classroom student case {index}",
            "Teachers report students using AI for classroom projects, homework feedback and future learning.",
            source=sources[(index + 4) % len(sources)],
            tags=["AI", "教育研究", "AI教育", "未来学习"],
            score=68 - index,
        )
        for index in range(4)
    ]
    learning_family_items = [
        make_item(
            f"Teen mental health and learning habits report {index}",
            "A public research report explains study habits, teen mental health, exam stress, sleep and parent-child relationship.",
            source=sources[(index + 8) % len(sources)],
            tags=["学习习惯", "青少年心理健康", "考试压力", "睡眠", "亲子关系"],
            score=60 - index,
        )
        for index in range(6)
    ]
    subject_items = [
        make_item(
            f"Reading motivation and math anxiety guide {index}",
            "Educators discuss reading motivation, math anxiety and better study routines for middle school students.",
            source=sources[(index + 2) % len(sources)],
            tags=["阅读兴趣", "数学焦虑", "学习方法"],
            score=52 - index,
        )
        for index in range(6)
    ]
    selected = select_top_picks(pure_ai_items + ai_education_items + learning_family_items + subject_items)
    families = [classify_topic_family(item) for item in selected]

    assert len(selected) == 20
    assert families.count("learning_psychology_family") >= 5
    assert families.count("pure_ai_tech") <= 5
    assert families.count("ai_education_student") >= 3


def test_learning_target_does_not_force_low_quality_items():
    pure_ai_items = [
        make_item(
            f"OpenAI product release {index}",
            "OpenAI announces model upgrade and enterprise developer tools.",
            tags=["AI", "科技巨头", "OpenAI"],
            score=58 - index,
        )
        for index in range(8)
    ]
    low_quality_psychology = [
        make_item(
            f"Anxiety marketing bootcamp {index}",
            "A limited-time course sale claims one simple trick cures anxiety and asks parents to sign up.",
            source="EdSurge",
            tags=["焦虑", "课程销售"],
        )
        for index in range(5)
    ]
    selected = select_top_picks(pure_ai_items + low_quality_psychology)
    titles = " ".join(item["title"] for item in selected)

    assert "Anxiety marketing bootcamp" not in titles
    assert len(selected) < 20


if __name__ == "__main__":
    test_topic_family_classification_and_scoring()
    test_top20_soft_balance_keeps_ai_education_and_limits_pure_ai()
    test_learning_target_does_not_force_low_quality_items()
    print("DIAGNOSIS: PASS")

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import (  # noqa: E402
    can_use_repeat_fallback,
    is_promotional_content,
    mark_duplicates,
    normalize_title,
    normalize_url,
    select_top_picks,
)


def make_item(
    index: int,
    *,
    title: str | None = None,
    link: str | None = None,
    source: str | None = None,
    summary: str = "A public education report examines how students learn and how families and schools can respond.",
    tags: list[str] | None = None,
    score: int = 60,
) -> dict:
    return {
        "title": title or f"Independent education research finding {index}",
        "link": link or f"https://example.org/research/{index}",
        "source": source or f"Research Source {index}",
        "source_category": "education_research",
        "published_at": "2026-06-30T00:00:00+00:00",
        "summary": summary,
        "tags": tags or ["教育研究", "儿童与青少年", "家庭教育"],
        "priority_score": score,
        "qiba_pitch": "这是一条可以转译给中国家长的教育研究和公共讨论。",
        "recommendation_level": "可收藏",
        "is_duplicate": False,
        "duplicate_reason": "",
        "first_seen_date": "",
        "last_selected_date": "",
        "allow_repeat": False,
    }


def make_seen(
    *,
    current_date: str = "2026-06-30",
    links: dict[str, str] | None = None,
    titles: dict[str, str] | None = None,
) -> dict:
    links = links or {}
    titles = titles or {}
    return {
        "links": links,
        "titles": titles,
        "first_links": dict(links),
        "first_titles": dict(titles),
        "current_date": current_date,
    }


def test_previous_day_same_url_and_tracking_variant_are_blocked():
    canonical = "https://example.org/story"
    item = make_item(1, link=f"{canonical}?utm_source=newsletter")
    mark_duplicates([item], make_seen(links={normalize_url(canonical): "2026-06-29"}))

    assert item["is_duplicate"]
    assert item["duplicate_reason"] == "same_link"
    assert item["last_selected_date"] == "2026-06-29"
    assert item["days_since_last_selected"] == 1
    assert item["duplicate_block_reason"] == "same_canonical_url_all_history"
    assert item["duplicate_match_type"] == "same_canonical_url_all_history"
    assert not can_use_repeat_fallback(item, current_date="2026-06-30")


def test_same_url_is_blocked_across_all_history():
    recent = make_item(2, link="https://example.org/seven-day-story")
    old = make_item(3, link="https://example.org/old-story")
    seen = make_seen(
        links={
            normalize_url(recent["link"]): "2026-06-24",
            normalize_url(old["link"]): "2026-06-22",
        }
    )
    mark_duplicates([recent, old], seen)

    assert recent["is_duplicate"]
    assert recent["same_url_recent_days"] == 6
    assert old["is_duplicate"]
    assert old["days_since_last_selected"] == 8
    assert old["duplicate_block_reason"] == "same_canonical_url_all_history"
    assert not can_use_repeat_fallback(old, current_date="2026-06-30")


def test_similar_title_is_blocked_across_all_history():
    previous_title = "New Study Explains Why Teen Sleep Improves Learning at School"
    item = make_item(
        4,
        title="New Study Explains How Teen Sleep Improves Learning in Schools",
        link="https://different.example.org/teen-sleep-study",
    )
    seen = make_seen(titles={normalize_title(previous_title): "2026-06-10"})
    mark_duplicates([item], seen)

    assert item["is_duplicate"]
    assert item["duplicate_reason"] == "similar_title"
    assert item["similar_title_recent_days"] == 20
    assert item["duplicate_block_reason"] == "similar_title_all_history"
    assert not can_use_repeat_fallback(item, current_date="2026-06-30")


def test_same_normalized_title_is_blocked_across_all_history():
    title = "Families Need Better Evidence About Student Screen Time"
    item = make_item(
        5,
        title="Families need better evidence about student screen-time!",
        link="https://different.example.org/screen-time-evidence",
    )
    seen = make_seen(titles={normalize_title(title): "2026-05-20"})
    mark_duplicates([item], seen)

    assert item["is_duplicate"]
    assert item["duplicate_reason"] == "same_title"
    assert item["duplicate_match_type"] == "same_normalized_title_all_history"
    assert not can_use_repeat_fallback(item, current_date="2026-06-30")


def test_promotional_calls_to_action_and_product_marketing_are_blocked():
    samples = [
        make_item(10, title="Join Our Webinar: Register Now for the AI Education Summit", score=95),
        make_item(11, title="Download the Guide to Our New Platform for Schools", score=95),
        make_item(12, title="New AI Product Launch and Free Trial for Teachers", score=95),
        make_item(
            13,
            title="Customer Story: Acme Schools Transform Learning With Our Platform",
            source="OpenAI Blog",
            score=95,
        ),
        make_item(14, title="Startup Files for IPO After New Funding Round", score=95),
    ]
    assert all(is_promotional_content(item) for item in samples)
    assert not select_top_picks(samples)


def test_authoritative_research_and_public_reporting_are_not_false_positives():
    research = make_item(
        20,
        title="University Study Finds Sleep Supports Teen Learning",
        summary="Peer-reviewed researchers followed students for two years and report evidence about sleep and memory.",
        source="University Research News",
        score=75,
    )
    public_event = make_item(
        21,
        title="Schools Respond After New Findings on Student Test Anxiety",
        summary="A public-interest investigation examines school support systems and family communication.",
        source="Public Education News",
        score=72,
    )

    assert not is_promotional_content(research)
    assert not is_promotional_content(public_event)
    selected = select_top_picks([research, public_event])
    assert {item["link"] for item in selected} == {research["link"], public_event["link"]}


def test_top20_still_fills_from_clean_candidates():
    clean_candidates = [make_item(100 + index, score=70 - (index % 10)) for index in range(25)]
    promotions = [
        make_item(200, title="Register Now for Our Education Webinar", score=99),
        make_item(201, title="Customer Story: Product Launch for Schools", source="OpenAI Blog", score=99),
    ]
    previous_day_repeat = make_item(202, title="Yesterday's Education Story", score=99)
    mark_duplicates(
        [previous_day_repeat],
        make_seen(links={normalize_url(previous_day_repeat["link"]): "2026-06-29"}),
    )

    selected = select_top_picks(clean_candidates + promotions + [previous_day_repeat], current_date="2026-06-30")
    assert len(selected) == 20
    assert all(not is_promotional_content(item) for item in selected)
    assert previous_day_repeat["link"] not in {item["link"] for item in selected}


if __name__ == "__main__":
    test_previous_day_same_url_and_tracking_variant_are_blocked()
    test_same_url_is_blocked_across_all_history()
    test_similar_title_is_blocked_across_all_history()
    test_same_normalized_title_is_blocked_across_all_history()
    test_promotional_calls_to_action_and_product_marketing_are_blocked()
    test_authoritative_research_and_public_reporting_are_not_false_positives()
    test_top20_still_fills_from_clean_candidates()
    print("DIAGNOSIS: PASS")

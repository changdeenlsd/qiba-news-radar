from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import (  # noqa: E402
    build_seasonal_item,
    item_text,
    load_keyword_rules,
    score_seasonal_relevance,
    select_daily_seasonal_topics,
    tag_item,
)


def make_item(title: str, summary: str, published_at: str = "2026-06-01T00:00:00+00:00") -> dict:
    return {
        "title": title,
        "summary": summary,
        "source": "Seasonal Test Source",
        "link": "https://example.com/seasonal/" + title.lower().replace(" ", "-"),
        "published_at": published_at,
        "source_category": "education_media",
        "priority_score": 50,
        "is_top_pick": False,
    }


def make_evergreen(title: str = "The Tale of Two Tables", window: str = "late_may_june", url: str | None = "https://www.edweek.org/education/opinion-the-tale-of-two-tables/2008/07") -> dict:
    return {
        "title": title,
        "url": url or "",
        "source": "Education Week",
        "original_year": 2008,
        "published_at": "2008-07-16",
        "language": "en",
        "region": "英文世界",
        "seasonal_windows": [window],
        "themes": ["暑假阅读", "暑假书单", "自主阅读", "阅读兴趣"],
        "evergreen_score": 90,
        "stale_risk": "low",
        "content_type": "经典重读",
        "topic_type": "seasonal_evergreen_fallback",
        "is_evergreen_fallback": True,
        "exclude_from_top20": True,
        "qiba_angle": "为什么暑假书单越长，孩子反而越不想读书？真正需要保护的是孩子自己选书的权利。",
        "why_still_relevant": "每年暑假前后，学校书单、指定阅读、阅读打卡和孩子自主选书都会重新成为家庭教育议题。",
        "notes": "旧文只作为本周时令选题 fallback，不进入 Top20。",
    }


def enrich(item: dict, rules: dict) -> dict:
    tags, directions = tag_item(item, rules)
    return {
        **item,
        "tags": tags,
        "directions": directions,
    }


def assert_seasonal(item: dict, today: str, expected_topics: set[str]) -> dict:
    seasonal = build_seasonal_item(item, today)
    selected = select_daily_seasonal_topics([item], today)
    assert selected, f"Expected seasonal item to be selected: {seasonal}"
    assert seasonal["seasonal_score"] >= 60, seasonal
    assert expected_topics & set(seasonal["seasonal_topics"]), seasonal
    return seasonal


def assert_all_have_urls(items: list[dict]) -> None:
    assert all(item.get("url") for item in items), items


def assert_not_seasonal(item: dict, today: str) -> dict:
    seasonal = build_seasonal_item(item, today)
    selected = select_daily_seasonal_topics([item], today)
    assert seasonal["seasonal_score"] < 60, seasonal
    assert not selected, f"Expected seasonal item to be rejected: {seasonal}"
    return seasonal


def main() -> int:
    rules = load_keyword_rules()
    samples = {
        "summer_reading": enrich(
            make_item(
                "The Tale of Two Tables: Summer Reading and Student Choice",
                "A teacher reflects on summer reading lists, required reading, student choice, independent reading and how schools can protect children's reading interest during summer.",
            ),
            rules,
        ),
        "final_exams": enrich(
            make_item(
                "How Parents Can Help Children Prepare for Final Exams Without Increasing Test Anxiety",
                "The article discusses exam preparation, review plans, sleep, parent support, test anxiety and end-of-term stress.",
            ),
            rules,
        ),
        "summer_sports": enrich(
            make_item(
                "Summer Sports and Swimming Safety for Children",
                "A guide about swimming safety, outdoor activities, heat protection, children's sports and summer exercise routines.",
                "2026-07-10T00:00:00+00:00",
            ),
            rules,
        ),
        "family_travel": enrich(
            make_item(
                "How Families Can Turn Summer Travel and Museum Visits into Learning",
                "The article explains family travel, museum education, science museum visits, children's curiosity and learning during summer trips.",
                "2026-07-15T00:00:00+00:00",
            ),
            rules,
        ),
        "camp_ad": enrich(
            make_item(
                "Limited-Time Summer Camp Enrollment Discount",
                "A training company promotes paid summer camp packages, limited-time discounts, consultation forms and sign-up bonuses.",
            ),
            rules,
        ),
        "travel_ad": enrich(
            make_item(
                "Top Luxury Resorts for Family Summer Vacation",
                "A travel platform recommends expensive resorts, hotel packages and shopping discounts, with little educational or child development value.",
            ),
            rules,
        ),
        "outdated_disney": enrich(
            make_item(
                "Disney Ticket Prices and Fast Pass Rules from 2017",
                "An old article lists outdated ticket prices, old fast pass rules and expired promotion details.",
                "2017-06-01T00:00:00+00:00",
            ),
            rules,
        ),
    }

    results = {
        "positive": [
            assert_seasonal(samples["summer_reading"], "2026-06-01", {"暑假阅读", "暑假书单", "自主阅读", "阅读兴趣"}),
            assert_seasonal(samples["final_exams"], "2026-06-01", {"期末考试", "期末复习", "考试焦虑"}),
            assert_seasonal(samples["summer_sports"], "2026-07-10", {"夏季运动", "游泳安全", "户外活动"}),
            assert_seasonal(samples["family_travel"], "2026-07-15", {"亲子游", "博物馆教育", "旅行学习"}),
        ],
        "negative": [
            assert_not_seasonal(samples["camp_ad"], "2026-06-01"),
            assert_not_seasonal(samples["travel_ad"], "2026-07-15"),
            assert_not_seasonal(samples["outdated_disney"], "2026-07-15"),
        ],
        "diagnostics": {
            key: {
                "tags": value["tags"],
                "score": score_seasonal_relevance(value, value["tags"], item_text(value, value["tags"]), "2026-06-01"),
                "text": item_text(value, value["tags"])[:180],
            }
            for key, value in samples.items()
        },
    }

    recent_three = [samples["summer_reading"], samples["final_exams"], enrich(make_item("Summer Reading Choice Guide for Families", "A recent article explains summer reading, required reading, independent reading, parents and children's reading interest."), rules)]
    selected_recent_three = select_daily_seasonal_topics(recent_three, "2026-06-01", [make_evergreen()])
    assert len(selected_recent_three) == 3, selected_recent_three
    assert all(item["topic_type"] in {"seasonal_recent", "seasonal_recent_analysis"} for item in selected_recent_three), selected_recent_three
    assert_all_have_urls(selected_recent_three)

    selected_evergreen_one = select_daily_seasonal_topics([], "2026-06-01", [make_evergreen()])
    assert len(selected_evergreen_one) == 1, selected_evergreen_one
    assert selected_evergreen_one[0]["topic_type"] == "seasonal_evergreen_fallback", selected_evergreen_one
    assert selected_evergreen_one[0]["url"], selected_evergreen_one

    evergreen_two = [make_evergreen(), make_evergreen("A Summer Reading Rights Classic", url="https://example.com/evergreen/summer-reading-rights")]
    selected_recent_one = select_daily_seasonal_topics([samples["summer_reading"]], "2026-06-01", evergreen_two)
    assert len(selected_recent_one) == 3, selected_recent_one
    assert selected_recent_one[0]["is_evergreen_fallback"] is False, selected_recent_one
    assert sum(1 for item in selected_recent_one if item["topic_type"] == "seasonal_evergreen_fallback") == 2, selected_recent_one
    assert_all_have_urls(selected_recent_one)

    selected_recent_two = select_daily_seasonal_topics([samples["summer_reading"], samples["final_exams"]], "2026-06-01", [make_evergreen()])
    assert len(selected_recent_two) == 3, selected_recent_two
    assert sum(1 for item in selected_recent_two if item["topic_type"] == "seasonal_evergreen_fallback") == 1, selected_recent_two
    assert_all_have_urls(selected_recent_two)

    selected_window_mismatch = select_daily_seasonal_topics([], "2026-06-01", [make_evergreen(window="january_february")])
    assert not selected_window_mismatch, selected_window_mismatch

    high_risk_evergreen = make_evergreen("Disney Ticket Prices and Fast Pass Rules from 2017", url="https://example.com/old-disney-prices")
    high_risk_evergreen["themes"] = ["迪士尼", "主题乐园"]
    high_risk_evergreen["stale_risk"] = "high"
    selected_high_risk = select_daily_seasonal_topics([], "2026-06-01", [high_risk_evergreen])
    assert not selected_high_risk, selected_high_risk

    no_url_recent = enrich(make_item("Summer Reading Without URL", "A recent article explains summer reading and student choice."), rules)
    no_url_recent["link"] = ""
    selected_no_url = select_daily_seasonal_topics([no_url_recent], "2026-06-01", [make_evergreen(url=None)])
    assert not selected_no_url, selected_no_url

    selected_noise = select_daily_seasonal_topics([samples["camp_ad"], samples["travel_ad"], samples["outdated_disney"]], "2026-07-15", [])
    assert not selected_noise, selected_noise

    results["link_only_selection"] = {
        "recent_three_count": len(selected_recent_three),
        "evergreen_one_count": len(selected_evergreen_one),
        "recent_one_plus_evergreen_count": len(selected_recent_one),
        "recent_two_plus_evergreen_count": len(selected_recent_two),
        "window_mismatch_blocked": not selected_window_mismatch,
        "high_risk_evergreen_blocked": not selected_high_risk,
        "no_url_blocked": not selected_no_url,
        "noise_blocked": not selected_noise,
    }

    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("\nDIAGNOSIS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

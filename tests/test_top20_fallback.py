from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_digest import select_top_picks  # noqa: E402


def make_item(
    index: int,
    *,
    title: str | None = None,
    source: str | None = None,
    score: int = 80,
    duplicate: bool = False,
    duplicate_reason: str = "same_link",
    first_seen_date: str = "2026-06-01",
    tags: list[str] | None = None,
    source_category: str = "",
    summary: str = "Students, parents and schools are learning how AI changes education and future learning.",
    link: str | None = None,
    topic_type: str = "",
    is_evergreen_fallback: bool = False,
) -> dict:
    item_title = title or f"High value education candidate {index}"
    return {
        "title": item_title,
        "link": link or f"https://example.com/top20/{index}-{item_title.lower().replace(' ', '-')}",
        "source": source or f"Test Source {index}",
        "source_category": source_category,
        "published_at": "2026-06-13T00:00:00+00:00",
        "summary": summary,
        "tags": tags or ["AI教育", "未来学习", "家庭教育"],
        "priority_score": score,
        "qiba_pitch": "这条内容适合七点半爸爸主稿，能转化为家庭教育和未来学习选题。",
        "is_duplicate": duplicate,
        "duplicate_reason": duplicate_reason if duplicate else "",
        "first_seen_date": first_seen_date if duplicate else "",
        "is_evergreen_fallback": is_evergreen_fallback,
        "topic_type": topic_type,
    }


def main() -> int:
    main_candidates = []
    for i in range(5):
        main_candidates.append(
            make_item(
                i,
                title=f"AI education classroom candidate {i}",
                score=80,
                duplicate=False,
                tags=["AI教育", "未来学习", "学生Builder"],
                summary="Students and teachers use AI in classroom learning, homework feedback and future skills.",
            )
        )
    for i in range(5, 9):
        main_candidates.append(
            make_item(
                i,
                title=f"Learning psychology candidate {i}",
                score=78,
                duplicate=False,
                tags=["学习习惯", "青少年心理健康", "家庭教育"],
                summary="Parents and schools support study habits, teen mental health and academic pressure with evidence-based guidance.",
            )
        )
    for i in range(9, 12):
        main_candidates.append(
            make_item(
                i,
                title=f"Subject learning candidate {i}",
                score=74,
                duplicate=False,
                tags=["阅读兴趣", "数学焦虑", "学习方法"],
                summary="Students build reading motivation, math confidence and learning methods in middle school.",
            )
        )
    for i in range(12, 14):
        main_candidates.append(
            make_item(
                i,
                title=f"Family education research candidate {i}",
                score=72,
                duplicate=False,
                tags=["家庭教育", "亲子关系", "屏幕时间"],
                summary="Families navigate screen time, parent-child relationships and school expectations.",
            )
        )

    fallback_specs = [
        ("Repeat high value AI education candidate 1", "OpenAI Blog", ["AI教育", "未来学习"], "Students use AI for learning and creativity in school."),
        ("Repeat high value AI education candidate 2", "Google for Education Blog", ["AI教育", "学生Builder"], "Teachers and students test AI learning workflows in classrooms."),
        ("Repeat high value study habits candidate", "Microsoft Education Blog", ["学习习惯", "自我管理"], "Students improve study habits, planning and self-regulation."),
        ("Repeat high value teen stress candidate", "MIT News", ["青少年心理健康", "考试压力"], "Research explains student stress, anxiety and school pressure."),
        ("Repeat high value reading candidate", "EdSurge", ["阅读兴趣", "学习动机"], "Students build reading motivation and durable learning habits."),
        ("Repeat high value family candidate", "Stanford HAI", ["家庭教育", "亲子关系", "屏幕时间"], "Families discuss screen time, attention and parent-child communication."),
    ]
    fallback_candidates = [
        make_item(100 + i, title=title, source=source, score=60, duplicate=True, tags=tags, summary=summary)
        for i, (title, source, tags, summary) in enumerate(fallback_specs, start=1)
    ]
    selected = select_top_picks(main_candidates + fallback_candidates, current_date="2026-06-13")
    assert len(selected) == 20, selected
    repeat_items = [item for item in selected if item.get("is_repeat_fallback")]
    assert len(repeat_items) == 6, repeat_items
    assert all(item.get("repeat_reason", "").startswith("duplicate:") for item in repeat_items), repeat_items
    assert all(item.get("top20_fill_reason") for item in repeat_items), repeat_items

    evergreen = make_item(
        201,
        title="Evergreen seasonal fallback should not enter",
        source="Education Week",
        score=95,
        duplicate=True,
        topic_type="seasonal_evergreen_fallback",
        is_evergreen_fallback=True,
    )
    seasonal = make_item(
        202,
        title="Seasonal fallback should not enter",
        source="Reading Rockets",
        score=95,
        duplicate=True,
        topic_type="seasonal_evergreen_fallback",
    )
    selected_without_seasonal = select_top_picks(main_candidates + fallback_candidates + [evergreen, seasonal], current_date="2026-06-13")
    assert all(item["title"] not in {evergreen["title"], seasonal["title"]} for item in selected_without_seasonal), selected_without_seasonal

    low_score = make_item(301, score=54, duplicate=True, tags=["AI教育"])
    selected_low_score = select_top_picks(main_candidates + [low_score], current_date="2026-06-13")
    assert low_score["link"] not in {item["link"] for item in selected_low_score}, selected_low_score

    ordinary_learning_resource = make_item(
        401,
        title="Ordinary learning resource duplicate",
        source="VOA Learning English - Education Tips",
        score=60,
        duplicate=True,
        source_category="learning_resource",
        tags=["家庭教育"],
        summary="A general school costs article without a direct high-value resource or major AI learning signal.",
    )
    selected_learning_resource = select_top_picks(main_candidates + [ordinary_learning_resource], current_date="2026-06-13")
    assert ordinary_learning_resource["link"] not in {item["link"] for item in selected_learning_resource}, selected_learning_resource

    recent_same_link = make_item(
        501,
        title="Yesterday duplicate same link should wait",
        source="MIT News",
        score=90,
        duplicate=True,
        duplicate_reason="same_link",
        first_seen_date="2026-06-12",
    )
    selected_recent_same_link = select_top_picks(main_candidates + [recent_same_link], current_date="2026-06-13")
    assert recent_same_link["link"] not in {item["link"] for item in selected_recent_same_link}, selected_recent_same_link

    same_title = make_item(
        601,
        title="High value same title can fill",
        source="MIT News",
        score=60,
        duplicate=True,
        duplicate_reason="same_title",
        first_seen_date="2026-06-12",
    )
    selected_same_title = select_top_picks(main_candidates + [same_title], current_date="2026-06-13")
    same_title_selected = [item for item in selected_same_title if item["link"] == same_title["link"]]
    assert same_title_selected and same_title_selected[0].get("is_repeat_fallback"), selected_same_title

    commercial = make_item(
        701,
        title="Commercial tutoring bootcamp discount",
        source="EdSurge",
        score=90,
        duplicate=True,
        summary="A tutoring company promotes a limited-time paid bootcamp and asks parents to sign up for a consultation.",
    )
    selected_commercial = select_top_picks(main_candidates + [commercial], current_date="2026-06-13")
    assert commercial["link"] not in {item["link"] for item in selected_commercial}, selected_commercial

    print(
        json.dumps(
            {
                "top20_fill_count": len(selected),
                "repeat_fallback_count": len(repeat_items),
                "low_score_blocked": low_score["link"] not in {item["link"] for item in selected_low_score},
                "learning_resource_blocked": ordinary_learning_resource["link"] not in {item["link"] for item in selected_learning_resource},
                "recent_same_link_blocked": recent_same_link["link"] not in {item["link"] for item in selected_recent_same_link},
                "same_title_allowed": bool(same_title_selected),
                "commercial_blocked": commercial["link"] not in {item["link"] for item in selected_commercial},
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print("\nDIAGNOSIS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

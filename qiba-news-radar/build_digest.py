from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
KEYWORDS_FILE = ROOT / "keywords.yml"
TOP_PICK_LIMIT = 20
MAX_TOP_PICKS_PER_SOURCE = 5


PRIORITY_SOURCES = {
    "OpenAI Blog": 24,
    "Google DeepMind Blog": 24,
    "Google AI Blog": 23,
    "Microsoft AI Blog": 23,
    "Meta AI Blog": 22,
    "NVIDIA Blog": 22,
    "MIT News": 24,
    "Stanford HAI": 24,
    "Harvard Graduate School of Education": 24,
    "EdWorkingPapers": 23,
    "MIT Technology Review": 21,
    "Quanta Magazine": 20,
    "Bloomberg Technology": 20,
    "Nature": 21,
    "Science": 21,
}

MEDIA_SOURCES = {
    "The Verge AI": 13,
    "TechCrunch AI": 12,
    "Ars Technica": 11,
    "Wired": 11,
}

THEME_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "chatgpt",
    "openai",
    "generative ai",
    "education",
    "learning",
    "student",
    "school",
    "university",
    "research",
    "children",
    "teen",
    "screen time",
    "ai tutor",
    "coding agent",
    "model",
    "robotics",
    "science education",
    "math",
    "tutoring",
    "skills",
    "confidence",
    "graduates",
    "automation",
    "workers",
    "wages",
    "jobs",
    "ai fluency",
    "universal learning",
    "olympiad",
]

AI_KEYWORDS = ["ai", "artificial intelligence", "chatgpt", "openai", "generative ai", "model", "coding agent"]
EDUCATION_KEYWORDS = ["education", "learning", "student", "school", "children", "teen", "ai tutor", "science education", "math", "tutoring", "skills"]
FIT_TAGS = {"教育研究", "AI教育", "儿童与青少年", "学习科学", "家庭教育", "媒介素养", "屏幕时间", "未来职业", "美国高校", "公办家庭可读", "教育热点"}
FAMILY_IMPACT_TAGS = {"OpenAI", "Google", "Microsoft", "Meta", "Apple", "Amazon", "NVIDIA", "科技巨头"}
DOWNRANK_KEYWORDS = [
    "podcast",
    "webinar",
    "event recap",
    "newsletter",
    "weekly roundup",
    "hiring",
    "job opening",
    "recruiting",
    "geforce now",
    "single sign-on",
    "gaming",
    "game streaming",
    "community investments",
    "subscriptions",
    "finance",
    "ads",
    "i/o",
]
ENTERPRISE_ONLY_KEYWORDS = ["enterprise", "developer", "coding agent", "sandbox", "infrastructure", "data center", "gpu", "partnership", "partners with", "cloud", "builders"]


def load_keyword_rules() -> dict:
    with KEYWORDS_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def latest_raw_file() -> Path:
    files = sorted(DATA_DIR.glob("*.raw.json"))
    if not files:
        raise FileNotFoundError("No raw news file found. Run fetch_news.py first.")
    return files[-1]


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def keyword_matches(text: str, keyword: str) -> bool:
    keyword = keyword.strip()
    if not keyword:
        return False
    if keyword.isascii() and re.fullmatch(r"[a-z0-9][a-z0-9 +.-]*", keyword, re.IGNORECASE):
        escaped = re.escape(keyword.lower())
        if keyword.isalpha() and len(keyword) > 2 and not keyword.endswith("s"):
            escaped = f"{escaped}s?"
        pattern = r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])"
        return re.search(pattern, text.lower()) is not None
    return keyword.lower() in text.lower()


def tag_item(item: dict, rules: dict) -> tuple[list[str], list[str]]:
    haystack = f"{item.get('title', '')} {item.get('summary', '')}"
    tags: list[str] = []
    directions: list[str] = []

    for tag_key, tag_rule in rules.get("tags", {}).items():
        if any(keyword_matches(haystack, keyword) for keyword in tag_rule.get("keywords", [])):
            tags.append(tag_rule.get("label", tag_key))
            directions.extend(rules.get("directions", {}).get(tag_key, []))

    if not directions:
        directions = rules.get("directions", {}).get("default", [])

    return tags or ["观察"], directions[:2]


def compact_chinese(text: str, limit: int = 92) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip("，。；、 ") + "。"


def source_actor(item: dict) -> str:
    source = item.get("source", "")
    title = clean_text(item.get("title", ""))
    text = f"{source} {title}".lower()
    actors = [
        ("openai", "OpenAI"),
        ("deepmind", "Google DeepMind"),
        ("google", "Google"),
        ("microsoft", "Microsoft"),
        ("meta", "Meta"),
        ("nvidia", "NVIDIA"),
        ("mit", "MIT"),
        ("stanford", "Stanford"),
        ("harvard", "Harvard"),
        ("techcrunch", "TechCrunch"),
        ("the verge", "The Verge"),
        ("quanta", "Quanta"),
    ]
    for keyword, actor in actors:
        if keyword in text:
            return actor
    return source.replace(" Blog", "").strip() or "相关机构"


def has_any(text: str, keywords: list[str]) -> bool:
    return any(keyword_matches(text, keyword) for keyword in keywords)


def detect_gartner_field(text: str) -> str:
    match = re.search(r"Magic Quadrant for ([^,.;]+)", text, re.IGNORECASE)
    if match:
        field = match.group(1).strip()
        field = re.sub(r"\benterprise\b", "企业级", field, flags=re.IGNORECASE)
        field = re.sub(r"\bai coding agents?\b", "AI 编程智能体", field, flags=re.IGNORECASE)
        return field
    if "coding agent" in text.lower():
        return "企业 AI 编程智能体"
    return "相关技术"


def detect_partner(text: str) -> str:
    patterns = [
        r"partners with ([^,.;]+)",
        r"partnership with ([^,.;]+)",
        r"with ([^,.;]+) to ",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            partner = clean_text(match.group(1))
            if 2 <= len(partner) <= 60:
                return partner
    return "外部机构"


def detect_research_focus(text: str) -> str:
    lower = text.lower()
    if has_any(lower, ["student", "learning", "school", "teacher", "classroom", "education"]):
        return "学生学习、学校教育或教学方式"
    if has_any(lower, ["child", "children", "teen", "youth", "adolescent", "screen time"]):
        return "儿童青少年与数字生活"
    if has_any(lower, ["model", "ai", "llm", "agent", "robot"]):
        return "AI 模型、智能体或技术应用"
    if has_any(lower, ["conjecture", "geometry", "theorem", "proof", "quantum", "biology", "math", "science"]):
        return "基础科学和前沿技术"
    return "一个值得跟踪的研究问题"


def build_zh_summary(item: dict, tags: list[str]) -> str:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    text = f"{title} {summary}"
    lower = text.lower()
    actor = source_actor(item)

    if has_any(lower, ["named a leader", "gartner", "magic quadrant"]):
        field = detect_gartner_field(text)
        return compact_chinese(f"{actor}被 Gartner 评为{field}领域领导者，重点信号是相关能力正在进入企业级采购和规模化部署阶段。", 80)

    if has_any(lower, ["partnership", "partners with", "content partnership", "collaboration"]):
        partner = detect_partner(text)
        return compact_chinese(f"{actor}与{partner}达成合作，核心看点是内容、技术或渠道资源被接入 AI 产品和服务生态。", 80)

    if has_any(lower, ["research", "study", "paper", "researchers", "scientists", "conjecture", "geometry", "theorem", "proof"]):
        focus = detect_research_focus(text)
        return compact_chinese(f"这项研究围绕{focus}展开，提供了新的发现、方法或比较框架，可作为后续分析的背景材料。", 80)

    if "codex" in lower:
        return compact_chinese("Codex 的应用案例显示，AI 编程工具正在从个人辅助走向团队协作和软件交付流程。", 80)

    if "with openai" in lower or "using openai" in lower:
        return compact_chinese("相关机构正在把 OpenAI 能力接入具体业务场景，重点是用 AI 改造服务流程和知识处理方式。", 80)

    if has_any(lower, ["student", "learning", "school", "teacher", "classroom", "education", "university"]):
        return compact_chinese("内容聚焦教育、学习或高校场景，适合关注技术变化如何影响学生、教师和家庭的日常选择。", 80)

    if has_any(lower, ["launch", "release", "introduces", "announces", "update", "new model", "tool"]):
        return compact_chinese(f"{actor}发布或更新了相关产品能力，重点在 AI 工具、平台功能或技术基础设施的持续演进。", 80)

    if "AI" in tags or "科技巨头" in tags:
        return compact_chinese(f"{actor}相关动态显示，AI 产品、平台生态或基础设施仍在快速变化，适合持续跟踪产业信号。", 80)

    return compact_chinese("相关动态提供了科技、研究或教育领域的新背景，可先记录关键信号，等待更明确的公共议题出现。", 80)


def build_story_angle(item: dict, tags: list[str]) -> str:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    text = f"{title} {summary}".lower()
    tag_set = set(tags)

    has_education = bool(
        tag_set
        & {
            "教育研究",
            "学习科学",
            "儿童与青少年",
            "媒介素养",
            "家庭教育",
            "屏幕时间",
            "未来职业",
            "AI教育",
        }
    ) or has_any(text, ["student", "learning", "school", "teacher", "children", "teen", "screen time", "education"])

    is_enterprise = has_any(text, ["enterprise", "gartner", "partnership", "partners with", "funding", "earnings", "developer", "coding agent"])
    is_research = has_any(text, ["research", "study", "paper", "university", "scientists"])

    if has_education and has_any(text, ["ai", "student", "learning", "school", "children", "screen time", "education"]):
        return compact_chinese("适合七点半爸爸主稿，可写成 AI、学校学习或数字生活如何进入普通家庭决策的角度，重点放在家长能理解的变化。", 100)

    if is_research:
        return compact_chinese("适合作为教育研究或科技背景资料，暂不急着写主稿；可积累为解释学习科学、AI 影响教育的证据线索。", 100)

    if is_enterprise:
        return compact_chinese("更适合做趋势观察或资料储备，关注 AI 工具从技术圈进入企业级市场；不建议直接作为七点半爸爸主稿。", 100)

    if "科技巨头" in tag_set or bool(tag_set & {"OpenAI", "Google", "Microsoft", "Meta", "NVIDIA", "Apple", "Amazon"}):
        return compact_chinese("可放入科技巨头动态观察，重点看平台、模型和生态变化；除非牵涉教育和青少年，否则不建议单独成稿。", 100)

    return compact_chinese("暂时适合作为选题储备，先记录其技术或研究背景；若后续出现教育、家庭或青少年关联，再考虑扩展成稿。", 100)


def build_qiba_pitch(item: dict, tags: list[str], priority_score: int) -> str:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    text = f"{title} {summary}"
    tag_set = set(tags)

    if has_any(text, ["olympiad", "math problems"]):
        return compact_chinese("适合写成教育选题，角度是“顶尖数学题库开放后，孩子怎样用 AI 和公开资源做深度学习”。可讨论题库、竞赛训练和自学能力，也提醒家长关注理解过程而不是刷题数量。", 120)

    if has_any(text, ["math", "tutoring", "student", "skills", "confidence"]) and has_any(text, ["ai", "artificial intelligence"]):
        return compact_chinese("适合写成主稿，角度可定为“AI 家教真的能帮孩子学数学吗”。重点解释工具如何提升练习反馈、信心和学习效率，同时提醒家长别把陪伴、诊断和鼓励完全交给系统。", 120)

    if has_any(text, ["ai fluency", "universal ai", "education for countries", "universal learning"]):
        return compact_chinese("适合写成文章，角度可定为“AI 素养会不会成为下一代基础能力”。可从国家、大学和平台都在推动 AI 教育切入，落到普通家庭如何启蒙、如何避免只学工具不学判断力。", 120)

    if has_any(text, ["automation", "workers", "wages", "jobs", "graduates", "career", "future of work"]):
        return compact_chinese("可写成未来职业观察，角度是“AI 和自动化正在改变年轻人的工作机会”。适合连接升学、专业选择和职业准备，但需要补充中国家庭能理解的行业案例，避免停留在海外职场新闻。", 120)

    if has_any(text, ["screen time", "spotify", "remix", "superfans", "social media", "pope"]):
        return compact_chinese("适合放入媒介素养资料库，观察 AI 内容、娱乐产品和公共讨论如何影响青少年数字生活。若没有儿童、学校或家庭冲突案例支撑，不建议单独成文，可等待更贴近家长的案例。", 120)

    if is_enterprise_only(title, summary, tags) or has_any(text, ["codex", "developer", "infrastructure", "cloud", "model", "protein", "chemical"]):
        return compact_chinese("更适合放入 AI 工具和技术趋势资料库，记录企业级应用、模型能力或基础设施变化。它离普通家长的日常问题较远，除非后续出现教育场景，不建议单独成文。", 120)

    if priority_score >= 65 and has_qiba_signal(title, summary, tags):
        return compact_chinese("适合写成文章，角度应从家长能感知的变化切入：学校、学习工具、孩子能力培养或未来职业。正文需要补充家庭或课堂场景，避免写成普通科技新闻摘要。", 120)

    if has_qiba_signal(title, summary, tags) or tag_set & FIT_TAGS:
        return compact_chinese("适合放入教育趋势资料库，后续可与学校学习、AI 教育、家庭教育或未来职业案例合并使用。单条信息力度有限，暂不建议单独成文，适合等同类案例成组后再写。", 120)

    return compact_chinese("适合放入科技背景资料库，主要用于跟踪 AI 公司、模型和平台生态变化。与普通家长、孩子学习关联较弱，不建议单独成文，只作为判断行业方向的辅助材料。", 120)


def normalize_qiba_pitch(text: str) -> str:
    if len(text) < 80:
        text = f"{text} 可作为早间选题会的辅助判断。"
    if len(text) < 80:
        text = f"{text} 后续可与同类新闻合并观察。"
    return compact_chinese(text, 120)


def parse_published_at(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def source_priority(source: str) -> int:
    if source in PRIORITY_SOURCES:
        return PRIORITY_SOURCES[source]
    if source in MEDIA_SOURCES:
        return MEDIA_SOURCES[source]
    return 8


def theme_priority(title: str, summary: str, tags: list[str]) -> int:
    text = f"{title} {summary} {' '.join(tags)}"
    score = 0
    for keyword in THEME_KEYWORDS:
        if keyword_matches(text, keyword):
            score += 4

    if has_any(text, AI_KEYWORDS) and has_any(text, EDUCATION_KEYWORDS):
        score += 10
    if keyword_matches(text, "research") and has_any(text, ["education", "learning", "student", "children"]):
        score += 6

    return min(score, 35)


def qiba_fit_priority(title: str, summary: str, tags: list[str]) -> int:
    text = f"{title} {summary}"
    tag_set = set(tags)
    score = 0

    score += min(len(tag_set & FIT_TAGS) * 6, 20)
    if "美国高校" in tag_set and has_any(text, ["research", "study", "learning", "student", "education"]):
        score += 6
    if (tag_set & FAMILY_IMPACT_TAGS) and has_any(text, ["family", "parent", "children", "student", "school", "learning", "education"]):
        score += 6
    if has_any(text, ["ai tutor", "personalized learning", "screen time", "media literacy", "child", "teen"]):
        score += 8

    return min(score, 30)


def recency_priority(published_at: str, now: datetime) -> int:
    published = parse_published_at(published_at)
    if not published:
        return 2
    if not published.tzinfo:
        published = published.replace(tzinfo=timezone.utc)
    age = now - published.astimezone(timezone.utc)
    if age.total_seconds() <= 24 * 60 * 60:
        return 10
    if age.total_seconds() <= 3 * 24 * 60 * 60:
        return 6
    return 2


def downrank_penalty(title: str, summary: str) -> int:
    text = f"{title} {summary}"
    penalty = 0
    for keyword in DOWNRANK_KEYWORDS:
        if keyword_matches(text, keyword):
            penalty += 16
    if has_any(text, ["marketing", "sponsored", "press release"]):
        penalty += 8
    return min(penalty, 25)


def has_qiba_signal(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return bool(set(tags) & FIT_TAGS) or has_any(
        text,
        ["education", "learning", "student", "school", "children", "teen", "parent", "family", "screen time", "media literacy", "ai tutor"],
    )


def is_enterprise_only(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return has_any(text, ENTERPRISE_ONLY_KEYWORDS) and not has_qiba_signal(title, summary, tags)


def calculate_priority_score(item: dict, tags: list[str], now: datetime) -> int:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    score = (
        source_priority(item.get("source", ""))
        + theme_priority(title, summary, tags)
        + qiba_fit_priority(title, summary, tags)
        + recency_priority(item.get("published_at", ""), now)
        - downrank_penalty(title, summary)
    )
    if not has_qiba_signal(title, summary, tags):
        score = min(score, 58)
    if is_enterprise_only(title, summary, tags):
        score = min(score - 12, 52)
    return max(0, min(100, score))


def recommendation_level(score: int) -> str:
    if score >= 85:
        return "必看"
    if score >= 70:
        return "可写"
    if score >= 55:
        return "可收藏"
    return "观察中"


def similarity_key(item: dict) -> tuple[str, str, str]:
    date = (item.get("published_at") or "")[:10]
    title = clean_text(item.get("title", "")).lower()
    words = re.findall(r"[a-z0-9]+", title)
    stop_words = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "with", "on", "by", "from", "how"}
    useful_words = [word for word in words if word not in stop_words]
    return (item.get("source", ""), date, " ".join(useful_words[:8]))


def select_top_picks(items: list[dict], limit: int = TOP_PICK_LIMIT) -> list[dict]:
    best_by_key: dict[tuple[str, str, str], dict] = {}
    for item in items:
        key = similarity_key(item)
        current = best_by_key.get(key)
        if current is None or item["priority_score"] > current["priority_score"]:
            best_by_key[key] = item

    ranked = sorted(best_by_key.values(), key=lambda item: (item["priority_score"], item.get("published_at", "")), reverse=True)
    selected: list[dict] = []
    source_counts: dict[str, int] = {}
    for item in ranked:
        source = item.get("source", "")
        if source_counts.get(source, 0) >= MAX_TOP_PICKS_PER_SOURCE:
            continue
        selected.append(item)
        source_counts[source] = source_counts.get(source, 0) + 1
        if len(selected) == limit:
            return selected

    if len(selected) < limit:
        selected_links = {item["link"] for item in selected}
        for item in ranked:
            if item["link"] in selected_links:
                continue
            selected.append(item)
            if len(selected) == limit:
                break
    return selected


def build_digest() -> tuple[Path, Path, Path, Path]:
    rules = load_keyword_rules()
    raw_file = latest_raw_file()
    date_text = raw_file.name.replace(".raw.json", "")
    raw_items = json.loads(raw_file.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)

    digest_items = []
    seen_links = set()
    for item in raw_items:
        link = item.get("link")
        if not link or link in seen_links:
            continue
        seen_links.add(link)
        tags, directions = tag_item(item, rules)
        zh_summary = build_zh_summary(item, tags)
        story_angle = build_story_angle(item, tags)
        priority_score = calculate_priority_score(item, tags, now)
        qiba_pitch = normalize_qiba_pitch(build_qiba_pitch(item, tags, priority_score))
        digest_items.append(
            {
                "title": clean_text(item.get("title", "")),
                "link": link,
                "source": item.get("source", ""),
                "published_at": item.get("published_at", ""),
                "summary": clean_text(item.get("summary", ""))[:300],
                "tags": tags,
                "zh_summary": zh_summary,
                "story_angle": story_angle,
                "qiba_pitch": qiba_pitch,
                "priority_score": priority_score,
                "recommendation_level": recommendation_level(priority_score),
                "is_top_pick": False,
                "directions": directions,
            }
        )

    top_items = select_top_picks(digest_items)
    top_links = {item["link"] for item in top_items}
    for item in digest_items:
        item["is_top_pick"] = item["link"] in top_links
    top_items = [item for item in digest_items if item["is_top_pick"]]
    top_items.sort(key=lambda item: (item["priority_score"], item.get("published_at", "")), reverse=True)

    json_file = DATA_DIR / f"{date_text}.json"
    md_file = DATA_DIR / f"{date_text}.md"
    top_json_file = DATA_DIR / f"{date_text}_top20.json"
    top_md_file = DATA_DIR / f"{date_text}_top20.md"
    json_file.write_text(json.dumps(digest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    md_file.write_text(render_markdown(date_text, digest_items, "七爸新闻雷达｜完整线索"), encoding="utf-8")
    top_json_file.write_text(json.dumps(top_items, ensure_ascii=False, indent=2), encoding="utf-8")
    top_md_file.write_text(render_markdown(date_text, top_items, "七爸新闻雷达｜今日精选 Top 20"), encoding="utf-8")
    render_html(date_text, top_items, len(digest_items))
    return json_file, md_file, top_json_file, top_md_file


def render_markdown(date_text: str, items: list[dict], title: str) -> str:
    lines = [f"# {title}", "", f"日期：{date_text}", f"数量：{len(items)}", ""]
    for index, item in enumerate(items, start=1):
        lines.extend(
            [
                f"## {index}. {item['title']}",
                f"- 来源：{item['source']}",
                f"- 发布时间：{item['published_at'] or '未知'}",
                f"- 优先级分数：{item['priority_score']}",
                f"- 推荐级别：{item['recommendation_level']}",
                f"- 标签：{', '.join(item['tags'])}",
                f"- 链接：{item['link']}",
                f"- 摘要：{item['summary'] or '暂无摘要'}",
                f"- 中文速读：{item['zh_summary']}",
                f"- 选题判断：{item['story_angle']}",
                f"- 七爸选题建议：{item['qiba_pitch']}",
                "",
            ]
        )
    return "\n".join(lines)


def render_html(date_text: str, items: list[dict], total_count: int) -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    groups = [
        ("今日必看", [item for item in items if item["priority_score"] >= 80]),
        ("可写成文章", [item for item in items if 65 <= item["priority_score"] <= 79]),
        ("资料储备", [item for item in items if item["priority_score"] < 65]),
    ]
    grouped_sections = "\n".join(render_group(title, group_items) for title, group_items in groups)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>七爸新闻雷达｜AI·科技·教育研究日报</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #1f2937; background: #f6f7f9; }}
    header {{ padding: 32px 20px 20px; background: #ffffff; border-bottom: 1px solid #e5e7eb; }}
    main {{ max-width: 960px; margin: 0 auto; padding: 24px 20px 48px; }}
    h1 {{ max-width: 960px; margin: 0 auto 8px; font-size: 28px; line-height: 1.25; }}
    .date {{ max-width: 960px; margin: 0 auto; color: #6b7280; }}
    .group {{ margin-bottom: 28px; }}
    .group-header {{ display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin: 0 0 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; }}
    .group-header h2 {{ margin: 0; font-size: 22px; line-height: 1.3; }}
    .group-count {{ color: #6b7280; font-size: 14px; white-space: nowrap; }}
    .empty {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; color: #6b7280; }}
    .item {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; margin-bottom: 16px; }}
    .meta {{ color: #6b7280; font-size: 14px; margin: 8px 0; }}
    .score-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0; color: #374151; font-size: 14px; }}
    .score-pill {{ background: #ecfdf5; color: #065f46; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .level-pill {{ background: #fff7ed; color: #9a3412; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0; }}
    .tag {{ background: #eef2ff; color: #3730a3; border-radius: 999px; padding: 3px 9px; font-size: 13px; }}
    .news-section {{ border-top: 1px solid #eef0f3; margin-top: 14px; padding-top: 12px; }}
    .news-section h3 {{ margin: 0 0 6px; font-size: 15px; line-height: 1.4; color: #111827; }}
    .news-section p {{ margin: 0; line-height: 1.7; }}
    .directions {{ margin: 0; padding-left: 20px; line-height: 1.7; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header>
    <h1>七爸新闻雷达｜AI·科技·教育研究日报</h1>
    <p class="date">日报日期：{escape(date_text)}｜今日精选 {len(items)} 条 / 原始线索共 {total_count} 条</p>
  </header>
  <main>
    {grouped_sections}
  </main>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")


def render_group(title: str, items: list[dict]) -> str:
    cards = "\n".join(render_card(item) for item in items)
    body = cards or '<p class="empty">暂无</p>'
    return f"""<section class="group">
  <div class="group-header">
    <h2>{escape(title)}</h2>
    <span class="group-count">{len(items)} 条</span>
  </div>
  {body}
</section>"""


def render_card(item: dict) -> str:
    tags = "".join(f'<span class="tag">{escape(tag)}</span>' for tag in item["tags"])
    return f"""<article class="item">
  <h2><a href="{escape(item['link'])}" target="_blank" rel="noopener noreferrer">{escape(item['title'])}</a></h2>
  <p class="meta">{escape(item['source'])}｜{escape(item['published_at'] or '发布时间未知')}</p>
  <div class="score-row">
    <span class="score-pill">优先级分数：{item['priority_score']}</span>
    <span class="level-pill">推荐级别：{escape(item['recommendation_level'])}</span>
  </div>
  <div class="tags">{tags}</div>
  <p>{escape(item['summary'] or '暂无摘要')}</p>
  <section class="news-section">
    <h3>中文速读</h3>
    <p>{escape(item.get('zh_summary') or '暂无中文速读')}</p>
  </section>
  <section class="news-section">
    <h3>选题判断</h3>
    <p>{escape(item.get('story_angle') or '暂无选题判断')}</p>
  </section>
  <section class="news-section">
    <h3>七爸选题建议</h3>
    <p>{escape(item.get('qiba_pitch') or '暂无七爸选题建议')}</p>
  </section>
</article>"""


def main() -> None:
    json_file, md_file, top_json_file, top_md_file = build_digest()
    print(f"Saved digest to {json_file} and {md_file}")
    print(f"Saved top picks to {top_json_file} and {top_md_file}")
    print(f"Updated {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    main()

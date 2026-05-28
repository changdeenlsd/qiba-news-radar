from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
KEYWORDS_FILE = ROOT / "keywords.yml"
REPORT_TZ = ZoneInfo("Asia/Shanghai")
TOP_PICK_LIMIT = 20
MAX_TOP_PICKS_PER_SOURCE = 3
MAX_SUPPLEMENTAL_EDUCATION_MEDIA_TOP_PICKS = 5
TOP20_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_top20\.json$")


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
    "Google for Education Blog": 20,
    "Microsoft Education Blog": 20,
    "MIT Technology Review": 21,
    "Quanta Magazine": 20,
    "Bloomberg Technology": 20,
    "Nature": 21,
    "Science": 21,
}

MEDIA_SOURCES = {
    "The Verge AI": 13,
    "TechCrunch AI": 12,
    "EdSurge": 8,
    "The 74": 4,
    "Inside Higher Ed": 4,
    "Times Higher Education": 4,
    "Ars Technica": 11,
    "Wired": 11,
}
SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES = {"The 74", "Inside Higher Ed", "Times Higher Education"}
EDUCATION_MEDIA_SOURCES = {"EdSurge"} | SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES
SUPPLEMENTAL_TOP_PICK_TAGS = {
    "AI时代学生画像",
    "AI教育",
    "学生Builder",
    "未来学习",
    "项目制学习",
    "家庭教育",
    "亲子教育",
    "K12教育",
    "教育公平",
    "学习能力",
    "科技教育",
    "心理健康",
    "阅读",
    "数学",
    "屏幕时间",
}
LOCAL_POLICY_STRONG_EXEMPTION_TAGS = {
    "AI时代学生画像",
    "AI教育",
    "学生Builder",
    "未来学习",
    "项目制学习",
    "科技教育",
}
LOCAL_POLICY_BROAD_EXEMPTION_TAGS = SUPPLEMENTAL_TOP_PICK_TAGS - LOCAL_POLICY_STRONG_EXEMPTION_TAGS

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
FIT_TAGS = {
    "教育研究",
    "AI教育",
    "儿童与青少年",
    "学习科学",
    "家庭教育",
    "媒介素养",
    "屏幕时间",
    "未来职业",
    "美国高校",
    "公办家庭可读",
    "教育热点",
}
HIGH_VALUE_EDUCATION_TAGS = {"AI时代学生画像", "学生Builder", "未来学习", "项目制学习"}
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
AI_STUDENT_SUBJECT_SIGNALS = [
    "student",
    "students",
    "high school",
    "college",
    "university",
    "campus",
    "class of",
    "cohort",
    "fellows",
    "young people",
    "young leaders",
    "teenagers",
    "undergraduate",
    "graduate",
    "student innovators",
    "young builders",
    "学生",
    "大学生",
    "高中生",
    "青年",
    "年轻人",
    "校园",
    "毕业生",
    "下一代",
    "入选者",
    "榜单",
    "学生创新者",
]
AI_STUDENT_TECH_SIGNALS = [
    "ai",
    "artificial intelligence",
    "chatgpt",
    "generative ai",
    "llm",
    "agents",
    "model",
    "openai",
    "deepmind",
    "anthropic",
    "microsoft",
    "google",
    "AI",
    "人工智能",
    "ChatGPT",
    "大模型",
    "生成式AI",
    "智能体",
    "OpenAI",
    "DeepMind",
    "Anthropic",
    "微软",
    "谷歌",
]
AI_STUDENT_PROJECT_SIGNALS = [
    "build",
    "create",
    "research",
    "discover",
    "solve",
    "prototype",
    "grant",
    "fellowship",
    "award",
    "selected",
    "named",
    "cohort",
    "project",
    "innovation",
    "social impact",
    "real-world problems",
    "创造",
    "开发",
    "研究",
    "发现",
    "解决",
    "项目",
    "资助",
    "奖学金",
    "入选",
    "榜单",
    "创新",
    "社会影响",
    "真实问题",
    "解决真实问题",
]
AI_STUDENT_STRONG_ACTION_SIGNALS = [
    "students build",
    "students create",
    "students developed",
    "students are using AI to",
    "students use AI to solve",
    "using AI to solve real-world problems",
    "student researchers",
    "student innovators",
    "young builders",
    "young AI leaders",
    "selected students",
    "student fellows",
    "AI fellows",
    "student grants",
    "students received grants",
    "students discover",
    "students research",
    "students launch projects",
    "students solve real-world problems",
    "ChatGPT Futures",
    "Class of",
    "学生开发",
    "学生创造",
    "学生用AI解决",
    "学生用人工智能解决",
    "学生研究者",
    "学生创新者",
    "学生项目",
    "学生获得资助",
    "学生入选",
    "学生榜单",
    "青年AI领导者",
    "年轻AI建设者",
    "学生发现",
    "学生研究",
    "学生做真实项目",
    "学生解决真实问题",
]
AI_EDU_TOOL_NEWS_KEYWORDS = [
    "AI tutor",
    "AI math tutor",
    "AI teaching assistant",
    "AI learning app",
    "edtech company launches",
    "education technology company launches",
    "AI classroom tool",
    "AI homework helper",
    "personalized learning platform",
    "adaptive learning platform",
    "AI-powered learning platform",
    "AI study app",
    "AI test prep",
    "K-12 AI tutor",
    "AI tutoring product",
    "AI家教",
    "AI数学家教",
    "AI学习机",
    "AI教育工具",
    "AI课堂工具",
    "AI作业助手",
    "AI刷题",
    "AI题库",
    "AI自适应学习",
    "AI个性化学习平台",
    "AI学习App",
    "AI教培产品",
    "AI培训产品",
    "AI助教产品",
]
AI_EDU_TOOL_CONTEXT_KEYWORDS = ["company", "startup", "platform", "product", "launches", "launched", "introduces", "edtech", "公司", "平台", "产品", "发布", "推出"]
EDUCATION_MEDIA_STRONG_RELEVANCE_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "generative ai",
    "chatgpt",
    "ai literacy",
    "future of learning",
    "future skills",
    "student project",
    "student innovation",
    "project-based learning",
    "real-world problem",
    "skills",
    "literacy",
    "creativity",
    "critical thinking",
    "parents",
    "parenting",
    "children",
    "kids",
    "k-12",
    "elementary",
    "middle school",
    "high school",
    "homework",
    "screen time",
    "college admissions pressure",
    "tutoring",
    "test prep",
    "assessment",
    "reading",
    "writing",
    "math",
    "stem",
    "mental health",
    "gifted",
    "career readiness",
    "AI",
    "人工智能",
    "生成式AI",
    "ChatGPT",
    "AI素养",
    "未来学习",
    "未来技能",
    "学生项目",
    "学生创新",
    "项目制学习",
    "真实问题",
    "能力",
    "素养",
    "创造力",
    "批判性思维",
    "家长",
    "父母",
    "孩子",
    "儿童",
    "中小学",
    "作业",
    "屏幕时间",
    "升学压力",
    "教培",
    "考试",
    "测评",
    "阅读",
    "写作",
    "数学",
    "STEM",
    "心理健康",
    "拔尖",
    "职业准备",
]
EDUCATION_MEDIA_NOISE_KEYWORDS = [
    "tuition",
    "commencement",
    "president",
    "board",
    "trustees",
    "admissions",
    "strike",
    "faculty",
    "state funding",
    "charter",
    "lawsuit",
    "superintendent",
    "district budget",
    "school board",
    "campus police",
    "athletics",
    "enrollment management",
    "collective bargaining",
    "tenure",
    "donor",
    "alumni",
    "ranking",
    "accreditation",
    "higher ed finance",
    "学费",
    "毕业典礼",
    "校长任命",
    "董事会",
    "招生办公室",
    "罢工",
    "教师工会",
    "州拨款",
    "特许学校",
    "诉讼",
    "学区预算",
    "校董会",
    "校园警察",
    "校友",
    "排名",
    "认证",
    "高校财政",
    "捐赠人",
]
LOCAL_US_EDUCATION_POLICY_NOISE_KEYWORDS = [
    "tuition",
    "state funding",
    "federal funding",
    "district budget",
    "school board",
    "board meeting",
    "superintendent",
    "trustees",
    "charter school policy",
    "voucher policy",
    "lawsuit",
    "court ruling",
    "strike",
    "union",
    "collective bargaining",
    "faculty contract",
    "campus police",
    "president appointment",
    "college president",
    "university president",
    "admissions office",
    "enrollment management",
    "accreditation",
    "ranking",
    "donor",
    "alumni",
    "commencement",
    "graduation ceremony",
    "public school funding",
    "public schools funding",
    "state legislature",
    "education bill",
    "local district",
    "county school",
    "school district",
    "feds",
    "federal money",
    "new money for public school",
    "funds",
    "funding",
    "closures",
    "waitlists",
    "学费",
    "州拨款",
    "联邦拨款",
    "学区预算",
    "校董会",
    "学校董事会",
    "学区会议",
    "教育局会议",
    "特许学校政策",
    "教育券",
    "诉讼",
    "法院裁决",
    "罢工",
    "教师工会",
    "集体谈判",
    "教师合同",
    "校园警察",
    "校长任命",
    "高校校长",
    "招生办公室",
    "招生管理",
    "认证",
    "排名",
    "捐赠人",
    "校友",
    "毕业典礼",
    "公立学校拨款",
    "州议会",
    "教育法案",
    "地方学区",
    "县学校",
    "学区治理",
]
LOCAL_POLICY_EXEMPTION_PARENT_CHILD_SIGNALS = [
    "parents",
    "parenting",
    "children",
    "kids",
    "k-12",
    "elementary",
    "middle school",
    "high school",
    "homework",
    "screen time",
    "家长",
    "父母",
    "孩子",
    "儿童",
    "中小学",
    "小学",
    "初中",
    "高中",
    "作业",
    "屏幕时间",
]
LOCAL_POLICY_EXEMPTION_LEARNING_SIGNALS = [
    "reading",
    "writing",
    "math",
    "stem",
    "learning skills",
    "critical thinking",
    "creativity",
    "assessment",
    "tutoring",
    "test prep",
    "gifted",
    "mental health",
    "阅读",
    "写作",
    "数学",
    "STEM",
    "学习能力",
    "批判性思维",
    "创造力",
    "测评",
    "教培",
    "考试",
    "拔尖",
    "心理健康",
]
LOCAL_POLICY_EXEMPTION_FUTURE_AI_SIGNALS = [
    "ai",
    "artificial intelligence",
    "chatgpt",
    "generative ai",
    "ai literacy",
    "future of learning",
    "future skills",
    "career readiness",
    "AI",
    "人工智能",
    "ChatGPT",
    "生成式AI",
    "AI素养",
    "未来学习",
    "未来技能",
    "职业准备",
]
GENERAL_TECH_RESERVE_NOISE_KEYWORDS = [
    "ai agent for taxes",
    "tax agent",
    "tax agents",
    "enterprise ai tool",
    "coding agent",
    "codex",
    "enterprise engineering",
    "engineering with codex",
    "developer tool",
    "api update",
    "cloud tool",
    "productivity tool",
    "workplace automation",
    "business automation",
    "stock trading",
    "trade stocks",
    "trading agent",
    "finance agent",
    "smart bird feeder",
    "smart home gadget",
    "wearable gadget",
    "camera gadget",
    "robot vacuum",
    "ai gadget",
    "consumer electronics",
    "protein design tool",
    "protein-design tool",
    "protein-design tools",
    "lab automation",
    "biotech platform",
    "materials discovery",
    "chemistry model",
    "drug discovery platform",
    "报税AI",
    "税务智能体",
    "企业AI工具",
    "编程智能体",
    "开发者工具",
    "API更新",
    "云服务工具",
    "办公自动化",
    "企业自动化",
    "智能喂鸟器",
    "智能家居小工具",
    "可穿戴设备",
    "摄像头小工具",
    "扫地机器人",
    "AI小玩意",
    "消费电子",
    "蛋白设计工具",
    "实验室自动化",
    "生物技术平台",
    "材料发现",
    "化学模型",
    "药物发现平台",
]
GENERAL_TECH_EDUCATION_TRANSLATION_SIGNALS = [
    "students",
    "student",
    "children",
    "kids",
    "parents",
    "parenting",
    "school",
    "k-12",
    "classroom",
    "homework",
    "learning",
    "education",
    "ai literacy",
    "future of learning",
    "student project",
    "project-based learning",
    "critical thinking",
    "creativity",
    "math",
    "reading",
    "writing",
    "screen time",
    "mental health",
    "college admissions",
    "career readiness",
    "学生",
    "孩子",
    "儿童",
    "家长",
    "父母",
    "学校",
    "中小学",
    "课堂",
    "作业",
    "学习",
    "教育",
    "AI素养",
    "未来学习",
    "学生项目",
    "项目制学习",
    "批判性思维",
    "创造力",
    "数学",
    "阅读",
    "写作",
    "屏幕时间",
    "心理健康",
    "升学",
    "职业准备",
]


def load_keyword_rules() -> dict:
    with KEYWORDS_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def report_date_today() -> str:
    return datetime.now(REPORT_TZ).strftime("%Y-%m-%d")


def latest_raw_file() -> Path:
    today_file = DATA_DIR / f"{report_date_today()}.raw.json"
    if today_file.exists():
        return today_file
    files = sorted(DATA_DIR.glob("*.raw.json"))
    if not files:
        raise FileNotFoundError("No raw news file found. Run fetch_news.py first.")
    return files[-1]


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def normalize_title(title: str) -> str:
    title = clean_text(title).lower()
    title = re.sub(r"\s+[-|]\s+(openai blog|microsoft ai blog|google ai blog|meta ai blog|nvidia blog|mit news|stanford hai|techcrunch|the verge).*?$", "", title)
    title = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


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


def is_ai_student_builder_topic(item: dict, tags: list[str], text: str | None = None) -> bool:
    text = text or f"{item.get('title', '')} {item.get('summary', '')} {' '.join(tags)}"
    tag_set = set(tags)
    has_strong_student_action = has_any(text, AI_STUDENT_STRONG_ACTION_SIGNALS)
    is_tool_product_news = has_any(text, AI_EDU_TOOL_NEWS_KEYWORDS) and has_any(text, AI_EDU_TOOL_CONTEXT_KEYWORDS)
    if is_tool_product_news and not has_strong_student_action:
        return False

    has_student_subject = has_any(text, AI_STUDENT_SUBJECT_SIGNALS) or bool(tag_set & {"AI时代学生画像", "学生Builder"})
    has_ai_signal = has_any(text, AI_STUDENT_TECH_SIGNALS)
    has_project_signal = has_any(text, AI_STUDENT_PROJECT_SIGNALS) or bool(tag_set & {"项目制学习"})
    if not (has_student_subject and has_ai_signal and has_project_signal and has_strong_student_action):
        return False

    matched_groups = sum(
        [
            has_student_subject,
            has_ai_signal,
            has_project_signal,
        ]
    )
    if matched_groups == 3:
        return True
    return matched_groups >= 2 and bool(tag_set & {"AI时代学生画像", "学生Builder"})


def ai_student_builder_bonus(item: dict, tags: list[str], text: str) -> int:
    tag_set = set(tags)
    if not is_ai_student_builder_topic(item, tags, text):
        return 0

    matched_groups = sum(
        [
            has_any(text, AI_STUDENT_SUBJECT_SIGNALS) or bool(tag_set & {"AI时代学生画像", "学生Builder"}),
            has_any(text, AI_STUDENT_TECH_SIGNALS),
            has_any(text, AI_STUDENT_PROJECT_SIGNALS) or bool(tag_set & {"项目制学习"}),
        ]
    )
    bonus = 0
    if matched_groups == 3:
        bonus += 8
    elif matched_groups >= 2 and bool(tag_set & {"AI时代学生画像", "学生Builder"}):
        bonus += 5
    if has_any(text, ["class of", "cohort", "fellows", "young leaders", "student innovators", "chatgpt futures"]):
        bonus += 3
    if has_any(text, ["grant", "fellowship", "selected", "award", "$10,000 grant"]):
        bonus += 2
    return bonus


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
            "AI时代学生画像",
            "学生Builder",
            "未来学习",
            "项目制学习",
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

    if (
        "AI时代学生画像" in tag_set
        or {"AI教育", "学生Builder"} <= tag_set
        or is_ai_student_builder_topic(item, tags, text)
    ):
        return compact_chinese("这条新闻可以转化为七爸选题：AI时代好学生画像正在变化。重点不是孩子会不会使用 AI 工具，而是能不能用 AI 解决真实问题、做出真实项目。适合延展到孩子该不该学 AI、项目制学习、英文资料检索和跨学科能力。", 120)

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


def has_education_media_relevance(text: str, tags: list[str]) -> bool:
    return bool(set(tags) & ({"AI教育", "屏幕时间", "家庭教育", "儿童与青少年", "未来职业"} | HIGH_VALUE_EDUCATION_TAGS)) or has_any(
        text,
        EDUCATION_MEDIA_STRONG_RELEVANCE_KEYWORDS,
    )


def is_education_media_noise(item: dict, source: str, tags: list[str], text: str) -> bool:
    if source not in EDUCATION_MEDIA_SOURCES:
        return False
    return has_any(text, EDUCATION_MEDIA_NOISE_KEYWORDS)


def is_local_us_education_policy_noise(item: dict, source: str, tags: list[str], text: str) -> bool:
    if source not in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
        return False
    return has_any(text, LOCAL_US_EDUCATION_POLICY_NOISE_KEYWORDS)


def education_media_penalty(item: dict, tags: list[str]) -> int:
    source = item.get("source", "")
    if source not in EDUCATION_MEDIA_SOURCES:
        return 0
    text = f"{item.get('title', '')} {item.get('summary', '')} {' '.join(tags)}"
    penalty = 0
    if not has_education_media_relevance(text, tags):
        penalty += 12 if source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES else 8
    if is_education_media_noise(item, source, tags, text):
        penalty += 10
    return min(penalty, 24)


def has_local_policy_noise_exemption(item: dict, tags: list[str], text: str) -> bool:
    tag_set = set(tags)
    if tag_set & LOCAL_POLICY_STRONG_EXEMPTION_TAGS:
        return True
    matched_groups = sum(
        [
            has_any(text, LOCAL_POLICY_EXEMPTION_PARENT_CHILD_SIGNALS),
            has_any(text, LOCAL_POLICY_EXEMPTION_LEARNING_SIGNALS),
            has_any(text, LOCAL_POLICY_EXEMPTION_FUTURE_AI_SIGNALS),
        ]
    )
    if matched_groups >= 2:
        return True
    if tag_set & LOCAL_POLICY_BROAD_EXEMPTION_TAGS:
        return matched_groups >= 1 and has_any(text, ["method", "practice", "classroom", "learning", "homework", "screen time", "mental health", "reading", "writing", "math", "AI", "人工智能", "方法", "课堂", "学习", "作业", "屏幕时间", "心理健康", "阅读", "写作", "数学"])
    score = int(item.get("priority_score") or 0)
    pitch = item.get("qiba_pitch", "")
    return score >= 82 and has_any(pitch, ["适合写成", "适合七点半爸爸主稿", "可以转化为七爸选题", "主稿"])


def is_general_tech_reserve_noise(item: dict, source: str, tags: list[str], text: str) -> bool:
    return has_any(text, GENERAL_TECH_RESERVE_NOISE_KEYWORDS)


def general_tech_reserve_can_enter_top20(item: dict) -> bool:
    source = item.get("source", "")
    tags = item.get("tags", [])
    text = f"{item.get('title', '')} {item.get('summary', '')} {' '.join(tags)}"
    score = int(item.get("priority_score") or 0)
    pitch = item.get("qiba_pitch", "")
    if source == "The Verge AI":
        if set(tags) & SUPPLEMENTAL_TOP_PICK_TAGS:
            return True
        if score >= 82 and has_any(pitch, ["适合写成", "适合七点半爸爸主稿", "可以转化为七爸选题", "主稿"]):
            return True
        return has_any(text, GENERAL_TECH_EDUCATION_TRANSLATION_SIGNALS) and not has_any(text, GENERAL_TECH_RESERVE_NOISE_KEYWORDS)
    if not is_general_tech_reserve_noise(item, source, tags, text):
        return True
    if set(tags) & SUPPLEMENTAL_TOP_PICK_TAGS:
        return True
    if has_any(text, GENERAL_TECH_EDUCATION_TRANSLATION_SIGNALS):
        return True
    return score >= 82 and has_any(pitch, ["适合写成", "适合七点半爸爸主稿", "可以转化为七爸选题", "主稿"])


def supplemental_education_media_can_enter_top20(item: dict) -> bool:
    source = item.get("source", "")
    if source not in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
        return True
    score = int(item.get("priority_score") or 0)
    tags = item.get("tags", [])
    text = f"{item.get('title', '')} {item.get('summary', '')} {' '.join(tags)}"
    if is_local_us_education_policy_noise(item, source, tags, text):
        return has_local_policy_noise_exemption(item, tags, text)
    return score >= 75 or has_education_media_relevance(text, tags) or bool(set(tags) & SUPPLEMENTAL_TOP_PICK_TAGS)


def has_qiba_signal(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return bool(set(tags) & (FIT_TAGS | HIGH_VALUE_EDUCATION_TAGS)) or has_any(
        text,
        ["education", "learning", "student", "school", "children", "teen", "parent", "family", "screen time", "media literacy", "ai tutor"],
    )


def is_enterprise_only(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return has_any(text, ENTERPRISE_ONLY_KEYWORDS) and not has_qiba_signal(title, summary, tags)


def calculate_priority_score(item: dict, tags: list[str], now: datetime) -> int:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    text = f"{title} {summary} {' '.join(tags)}"
    score = (
        source_priority(item.get("source", ""))
        + theme_priority(title, summary, tags)
        + qiba_fit_priority(title, summary, tags)
        + recency_priority(item.get("published_at", ""), now)
        - downrank_penalty(title, summary)
        - education_media_penalty(item, tags)
        + ai_student_builder_bonus(item, tags, text)
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


def load_seen_items(data_dir: Path, current_date: str) -> dict:
    seen = {
        "links": {},
        "titles": {},
        "history_files": [],
        "used_history_files": [],
        "item_count": 0,
    }
    for path in sorted(data_dir.glob("*_top20.json")):
        match = TOP20_FILE_RE.match(path.name)
        if not match:
            continue
        file_date = match.group(1)
        seen["history_files"].append(str(path))
        if file_date >= current_date:
            continue
        try:
            items = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        seen["used_history_files"].append(str(path))
        for item in items:
            seen["item_count"] += 1
            link = item.get("link", "").strip()
            title = clean_text(item.get("title", ""))
            normalized = item.get("normalized_title") or normalize_title(title)
            if link and link not in seen["links"]:
                seen["links"][link] = file_date
            if normalized and normalized not in seen["titles"]:
                seen["titles"][normalized] = file_date
    return seen


def similar_seen_title(normalized_title: str, seen_titles: dict[str, str]) -> tuple[bool, str]:
    if not normalized_title or len(normalized_title) <= 20:
        return False, ""
    for seen_title, first_seen_date in seen_titles.items():
        if len(seen_title) <= 20:
            continue
        if normalized_title in seen_title or seen_title in normalized_title:
            return True, first_seen_date
    return False, ""


def mark_duplicates(items: list[dict], seen_items: dict) -> int:
    duplicate_count = 0
    seen_links = seen_items.get("links", {})
    seen_titles = seen_items.get("titles", {})
    for item in items:
        link = item.get("link", "").strip()
        normalized = normalize_title(item.get("title", ""))
        item["normalized_title"] = normalized
        item["is_duplicate"] = False
        item["duplicate_reason"] = ""
        item["first_seen_date"] = ""
        item["allow_repeat"] = False

        if link in seen_links:
            item["is_duplicate"] = True
            item["duplicate_reason"] = "same_link"
            item["first_seen_date"] = seen_links[link]
        elif normalized in seen_titles:
            item["is_duplicate"] = True
            item["duplicate_reason"] = "same_title"
            item["first_seen_date"] = seen_titles[normalized]
        else:
            is_similar, first_seen_date = similar_seen_title(normalized, seen_titles)
            if is_similar:
                item["is_duplicate"] = True
                item["duplicate_reason"] = "similar_title"
                item["first_seen_date"] = first_seen_date

        if item["is_duplicate"]:
            duplicate_count += 1
    return duplicate_count


def build_archive_index(data_dir: Path) -> tuple[list[dict], dict[str, list[dict]]]:
    archive_index: list[dict] = []
    archive_data: dict[str, list[dict]] = {}
    for path in sorted(data_dir.glob("*_top20.json"), reverse=True):
        match = TOP20_FILE_RE.match(path.name)
        if not match:
            continue
        date_text = match.group(1)
        try:
            top_items = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        archive_data[date_text] = top_items
        full_file = data_dir / f"{date_text}.json"
        total_count = None
        duplicate_count = None
        if full_file.exists():
            try:
                full_items = json.loads(full_file.read_text(encoding="utf-8"))
                total_count = len(full_items)
                duplicate_count = sum(1 for item in full_items if item.get("is_duplicate"))
            except json.JSONDecodeError:
                pass
        entry = {
            "date": date_text,
            "top20File": f"data/{date_text}_top20.json",
            "count": len(top_items),
        }
        if total_count is not None:
            entry["totalCount"] = total_count
        if duplicate_count is not None:
            entry["duplicateCount"] = duplicate_count
        archive_index.append(entry)

    archive_index.sort(key=lambda entry: entry["date"], reverse=True)
    archive_data = {entry["date"]: archive_data[entry["date"]] for entry in archive_index}
    return archive_index, archive_data


def select_top_picks(items: list[dict], limit: int = TOP_PICK_LIMIT) -> list[dict]:
    best_by_key: dict[tuple[str, str, str], dict] = {}
    for item in [candidate for candidate in items if not candidate.get("is_duplicate")]:
        key = similarity_key(item)
        current = best_by_key.get(key)
        if current is None or item["priority_score"] > current["priority_score"]:
            best_by_key[key] = item

    ranked = sorted(best_by_key.values(), key=lambda item: (item["priority_score"], item.get("published_at", "")), reverse=True)
    selected: list[dict] = []
    source_counts: dict[str, int] = {}
    supplemental_education_media_count = 0
    for item in ranked:
        source = item.get("source", "")
        score = int(item.get("priority_score") or 0)
        is_high_score = score >= 80
        if not general_tech_reserve_can_enter_top20(item):
            continue
        if not supplemental_education_media_can_enter_top20(item):
            continue
        if not is_high_score and source_counts.get(source, 0) >= MAX_TOP_PICKS_PER_SOURCE:
            continue
        if (
            not is_high_score
            and source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES
            and supplemental_education_media_count >= MAX_SUPPLEMENTAL_EDUCATION_MEDIA_TOP_PICKS
        ):
            continue
        selected.append(item)
        source_counts[source] = source_counts.get(source, 0) + 1
        if source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
            supplemental_education_media_count += 1
        if len(selected) == limit:
            return selected
    return selected


def build_digest() -> tuple[Path, Path, Path, Path]:
    rules = load_keyword_rules()
    raw_file = latest_raw_file()
    date_text = raw_file.name.replace(".raw.json", "")
    raw_items = json.loads(raw_file.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    seen_items = load_seen_items(DATA_DIR, date_text)

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
                "normalized_title": normalize_title(item.get("title", "")),
                "zh_summary": zh_summary,
                "story_angle": story_angle,
                "qiba_pitch": qiba_pitch,
                "priority_score": priority_score,
                "recommendation_level": recommendation_level(priority_score),
                "is_top_pick": False,
                "is_duplicate": False,
                "duplicate_reason": "",
                "first_seen_date": "",
                "allow_repeat": False,
                "directions": directions,
            }
        )

    duplicate_count = mark_duplicates(digest_items, seen_items)
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
    archive_index_file = DATA_DIR / "archive_index.json"
    json_file.write_text(json.dumps(digest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    md_file.write_text(render_markdown(date_text, digest_items, "七爸新闻雷达｜完整线索"), encoding="utf-8")
    top_json_file.write_text(json.dumps(top_items, ensure_ascii=False, indent=2), encoding="utf-8")
    top_md_file.write_text(render_markdown(date_text, top_items, "七爸新闻雷达｜今日精选 Top 20"), encoding="utf-8")
    archive_index, archive_data = build_archive_index(DATA_DIR)
    archive_index_file.write_text(json.dumps(archive_index, ensure_ascii=False, indent=2), encoding="utf-8")
    render_html(date_text, top_items, len(digest_items), duplicate_count, archive_index, archive_data)
    print(f"History top20 files found: {len(seen_items['history_files'])}")
    print(f"History top20 files used: {len(seen_items['used_history_files'])}")
    print(f"History top20 items collected: {seen_items['item_count']}")
    print(f"Filtered duplicate candidates: {duplicate_count}")
    print(f"Updated archive index: {archive_index_file}")
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
                f"- 是否重复：{item['is_duplicate']}",
                f"- 重复原因：{item['duplicate_reason'] or '无'}",
                f"- 首次推送日期：{item['first_seen_date'] or '无'}",
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


def script_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_html(
    date_text: str,
    items: list[dict],
    total_count: int,
    duplicate_count: int,
    archive_index: list[dict],
    archive_data: dict[str, list[dict]],
) -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    groups = [
        ("今日必看", [item for item in items if item["priority_score"] >= 80]),
        ("可写成文章", [item for item in items if 65 <= item["priority_score"] <= 79]),
        ("资料储备", [item for item in items if item["priority_score"] < 65]),
    ]
    grouped_sections = "\n".join(render_group(title, group_items) for title, group_items in groups)
    shortage_notice = ""
    if len(items) < TOP_PICK_LIMIT:
        shortage_notice = f'<p class="notice">今日去重后不足20条，实际显示 {len(items)} 条。</p>'
    archive_index_json = script_json(archive_index)
    archive_data_json = script_json(archive_data)
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
    .archive-control {{ max-width: 960px; margin: 16px auto 0; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
    .archive-control label {{ color: #374151; font-weight: 600; }}
    .archive-control select {{ min-width: 180px; border: 1px solid #d1d5db; border-radius: 8px; padding: 7px 10px; background: #ffffff; color: #111827; }}
    .notice {{ max-width: 960px; margin: 10px auto 0; color: #9a3412; font-weight: 600; }}
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
    <p class="date" id="archive-meta">日报日期：{escape(date_text)}｜今日精选 {len(items)} 条 / 原始线索共 {total_count} 条 / 已过滤重复 {duplicate_count} 条</p>
    <div class="archive-control">
      <label for="archive-date">选择日报日期</label>
      <select id="archive-date" aria-label="选择日报日期"></select>
    </div>
    <p class="notice" id="archive-notice">{shortage_notice.replace('<p class="notice">', '').replace('</p>', '')}</p>
  </header>
  <main id="digest-content">
    {grouped_sections}
  </main>
  <script id="archive-index-data" type="application/json">{archive_index_json}</script>
  <script id="archive-items-data" type="application/json">{archive_data_json}</script>
  <script>
    const embeddedArchiveIndex = JSON.parse(document.getElementById("archive-index-data").textContent);
    const embeddedArchiveData = JSON.parse(document.getElementById("archive-items-data").textContent);
    let archiveIndex = embeddedArchiveIndex;
    const archiveCache = {{ ...embeddedArchiveData }};

    const dateSelect = document.getElementById("archive-date");
    const metaEl = document.getElementById("archive-meta");
    const noticeEl = document.getElementById("archive-notice");
    const contentEl = document.getElementById("digest-content");

    function escapeHtml(value) {{
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }}

    function groupItems(items) {{
      return [
        ["今日必看", items.filter((item) => Number(item.priority_score || 0) >= 80)],
        ["可写成文章", items.filter((item) => Number(item.priority_score || 0) >= 65 && Number(item.priority_score || 0) <= 79)],
        ["资料储备", items.filter((item) => Number(item.priority_score || 0) < 65)],
      ];
    }}

    function renderCard(item) {{
      const tags = (item.tags || []).map((tag) => `<span class="tag">${{escapeHtml(tag)}}</span>`).join("");
      return `<article class="item">
  <h2><a href="${{escapeHtml(item.link)}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(item.title)}}</a></h2>
  <p class="meta">${{escapeHtml(item.source)}}｜${{escapeHtml(item.published_at || "发布时间未知")}}</p>
  <div class="score-row">
    <span class="score-pill">优先级分数：${{escapeHtml(item.priority_score ?? "")}}</span>
    <span class="level-pill">推荐级别：${{escapeHtml(item.recommendation_level || "")}}</span>
  </div>
  <div class="tags">${{tags}}</div>
  <p>${{escapeHtml(item.summary || "暂无摘要")}}</p>
  <section class="news-section">
    <h3>中文速读</h3>
    <p>${{escapeHtml(item.zh_summary || "暂无中文速读")}}</p>
  </section>
  <section class="news-section">
    <h3>选题判断</h3>
    <p>${{escapeHtml(item.story_angle || "暂无选题判断")}}</p>
  </section>
  <section class="news-section">
    <h3>七爸选题建议</h3>
    <p>${{escapeHtml(item.qiba_pitch || "暂无七爸选题建议")}}</p>
  </section>
</article>`;
    }}

    function renderGroup(title, items) {{
      const body = items.length ? items.map(renderCard).join("") : '<p class="empty">暂无</p>';
      return `<section class="group">
  <div class="group-header">
    <h2>${{escapeHtml(title)}}</h2>
    <span class="group-count">${{items.length}} 条</span>
  </div>
  ${{body}}
</section>`;
    }}

    function updateMeta(entry, items) {{
      if (Number.isFinite(entry.totalCount) && Number.isFinite(entry.duplicateCount)) {{
        metaEl.textContent = `日报日期：${{entry.date}}｜今日精选 ${{items.length}} 条 / 原始线索共 ${{entry.totalCount}} 条 / 已过滤重复 ${{entry.duplicateCount}} 条`;
      }} else {{
        metaEl.textContent = `日报日期：${{entry.date}}｜今日精选 ${{items.length}} 条 / 历史归档`;
      }}
      noticeEl.textContent = items.length < {TOP_PICK_LIMIT} ? `今日去重后不足20条，实际显示 ${{items.length}} 条。` : "";
    }}

    function renderArchive(entry, items) {{
      updateMeta(entry, items);
      contentEl.innerHTML = groupItems(items).map(([title, group]) => renderGroup(title, group)).join("");
      dateSelect.value = entry.date;
      const url = new URL(window.location.href);
      url.searchParams.set("date", entry.date);
      window.history.replaceState(null, "", url);
    }}

    async function loadArchiveIndex() {{
      try {{
        const response = await fetch("../data/archive_index.json", {{ cache: "no-store" }});
        if (!response.ok) throw new Error("archive index not found");
        archiveIndex = await response.json();
      }} catch (error) {{
        archiveIndex = embeddedArchiveIndex;
      }}
    }}

    async function loadArchiveItems(entry) {{
      if (archiveCache[entry.date]) return archiveCache[entry.date];
      try {{
        const response = await fetch(`../${{entry.top20File}}`, {{ cache: "no-store" }});
        if (!response.ok) throw new Error("archive file not found");
        const items = await response.json();
        archiveCache[entry.date] = items;
        return items;
      }} catch (error) {{
        if (embeddedArchiveData[entry.date]) return embeddedArchiveData[entry.date];
        throw error;
      }}
    }}

    function populateDateSelect() {{
      dateSelect.innerHTML = archiveIndex
        .map((entry) => `<option value="${{escapeHtml(entry.date)}}">${{escapeHtml(entry.date)}}</option>`)
        .join("");
    }}

    async function showDate(date) {{
      const entry = archiveIndex.find((item) => item.date === date) || archiveIndex[0];
      if (!entry) return;
      try {{
        const items = await loadArchiveItems(entry);
        renderArchive(entry, items);
      }} catch (error) {{
        noticeEl.textContent = "该日期归档加载失败，请检查 data 文件是否存在。";
      }}
    }}

    async function initArchiveBrowser() {{
      await loadArchiveIndex();
      populateDateSelect();
      const params = new URLSearchParams(window.location.search);
      const requestedDate = params.get("date");
      await showDate(requestedDate || archiveIndex[0]?.date);
    }}

    dateSelect.addEventListener("change", () => showDate(dateSelect.value));
    initArchiveBrowser();
  </script>
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

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
KEYWORDS_FILE = ROOT / "keywords.yml"
EVERGREEN_SEASONAL_FILE = ROOT / "evergreen_seasonal.yml"
REPORT_TZ = ZoneInfo("Asia/Shanghai")
TOP_PICK_LIMIT = 20
RESOURCE_PICK_LIMIT = 5
RESOURCE_MIN_SCORE = 65
SEASONAL_PICK_LIMIT = 3
SEASONAL_TARGET_COUNT = 3
SEASONAL_PERIOD = "weekly"
SEASONAL_MIN_SCORE = 60
EVERGREEN_SEASONAL_MIN_SCORE = 75
MAX_TOP_PICKS_PER_SOURCE = 3
MAX_SUPPLEMENTAL_EDUCATION_MEDIA_TOP_PICKS = 5
REPEAT_FALLBACK_MIN_SCORE = 58
REPEAT_FALLBACK_TAG_MIN_SCORE = 55
AI_TECH_SOFT_CAP = 10
PURE_AI_TECH_SOFT_CAP = 5
LEARNING_PSYCH_FAMILY_TARGET = 5
TOPIC_FAMILY_RELAXED_MIN_SCORE = 28
TOP20_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_top20\.json$")
RESOURCE_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_resources\.json$")
SEASONAL_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_seasonal\.json$")


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
    "Child Mind Institute": 18,
    "ScienceDaily Education": 17,
    "ScienceDaily Mind & Brain": 16,
    "The Conversation US Education": 14,
    "The Conversation UK Education": 14,
    "Greater Good Magazine": 13,
    "Neuroscience News": 12,
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
BROAD_WELLBEING_RESEARCH_SOURCES = {
    "Greater Good Magazine",
    "ScienceDaily Education",
    "ScienceDaily Mind & Brain",
    "Neuroscience News",
}
BROAD_WELLBEING_CONTEXT_KEYWORDS = [
    "student",
    "students",
    "school",
    "schools",
    "teacher",
    "teachers",
    "classroom",
    "education",
    "learning",
    "homework",
    "parent",
    "parents",
    "parenting",
    "family",
    "families",
    "child",
    "children",
    "kid",
    "kids",
    "teen",
    "teens",
    "adolescent",
    "adolescents",
    "youth",
    "exam",
    "test anxiety",
    "academic pressure",
    "screen time",
    "sleep",
    "attention",
    "reading",
    "math",
    "学生",
    "学校",
    "教育",
    "学习",
    "课堂",
    "教师",
    "家长",
    "父母",
    "家庭",
    "孩子",
    "儿童",
    "青少年",
    "青春期",
    "考试",
    "学业压力",
    "屏幕时间",
    "睡眠",
    "注意力",
]
BROAD_WELLBEING_MEDICAL_NOISE_KEYWORDS = [
    "older adults",
    "middle age",
    "elderly",
    "70s",
    "80s",
    "cancer",
    "chemotherapy",
    "patients",
    "patient",
    "embryo",
    "maternal age",
    "glp-1",
    "biomarker",
    "saliva",
    "dopamine",
    "autophagy",
    "substance use",
    "clinical trial",
    "drug",
    "therapy",
    "therapies",
    "老年",
    "中年",
    "癌症",
    "化疗",
    "患者",
    "胚胎",
    "药物",
    "临床",
]
BROAD_WELLBEING_STRONG_CONTEXT_KEYWORDS = [
    "student",
    "students",
    "school",
    "schools",
    "teacher",
    "teachers",
    "classroom",
    "education",
    "homework",
    "parent",
    "parents",
    "parenting",
    "family",
    "families",
    "child",
    "children",
    "kid",
    "kids",
    "teen",
    "teens",
    "adolescent",
    "adolescents",
    "youth",
    "exam",
    "academic pressure",
    "screen time",
    "学生",
    "学校",
    "教育",
    "课堂",
    "教师",
    "家长",
    "父母",
    "家庭",
    "孩子",
    "儿童",
    "青少年",
    "青春期",
    "考试",
    "学业压力",
    "屏幕时间",
]
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
    "青少年心理健康",
    "考试压力",
    "考试焦虑",
    "学习习惯",
    "学习方法",
    "学习动机",
    "脑科学",
    "认知科学",
    "亲子关系",
    "睡眠",
    "运动与学习",
    "阅读",
    "阅读兴趣",
    "数学",
    "数学焦虑",
    "屏幕时间",
}
LEARNING_RESOURCE_MAJOR_TOP_PICK_TAGS = {
    "AI时代学生画像",
    "AI教育",
    "学生Builder",
    "未来学习",
    "项目制学习",
    "屏幕时间",
    "心理健康",
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
    "parents",
    "family",
    "university",
    "research",
    "children",
    "teen",
    "adolescent",
    "mental health",
    "test anxiety",
    "exam stress",
    "study habits",
    "learning science",
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
TECH_NEWS_SOURCES = {"TechCrunch AI", "The Verge AI", "NVIDIA Blog", "MIT Technology Review", "Google AI Blog", "OpenAI Blog", "Google DeepMind Blog", "Microsoft AI Blog", "Meta AI Blog"}
EDUCATION_KEYWORDS = ["education", "learning", "student", "school", "parents", "family", "children", "teen", "adolescent", "ai tutor", "science education", "math", "tutoring", "skills"]
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
REPEAT_FALLBACK_HIGH_VALUE_TAGS = {
    "AI教育",
    "AI时代学生画像",
    "学生Builder",
    "未来学习",
    "项目制学习",
    "屏幕时间",
    "心理健康",
    "青少年心理健康",
    "考试压力",
    "考试焦虑",
    "学习习惯",
    "学习方法",
    "学习动机",
    "脑科学",
    "认知科学",
    "家庭教育",
    "亲子关系",
    "睡眠",
    "运动与学习",
    "数学学习",
    "数学焦虑",
    "数学",
    "阅读教育",
    "阅读兴趣",
    "阅读",
}
REPEAT_FALLBACK_PREFERRED_SOURCES = {
    "OpenAI Blog",
    "Google for Education Blog",
    "Microsoft Education Blog",
    "MIT News",
    "EdSurge",
    "Stanford HAI",
    "Harvard Graduate School of Education",
    "Google AI Blog",
}
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
    "ipo",
    "benchmark",
    "model upgrade",
    "developer tool",
    "cloud service",
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
PURE_AI_TECH_KEYWORDS = [
    "launches",
    "announces",
    "introduces",
    "new model",
    "model upgrade",
    "benchmark",
    "infrastructure",
    "data center",
    "gpu",
    "chip",
    "developer",
    "coding agent",
    "api",
    "cloud",
    "enterprise",
    "partnership",
    "ipo",
    "funding",
    "financing",
    "subscription",
    "productivity",
    "发布",
    "推出",
    "模型升级",
    "基准测试",
    "基础设施",
    "数据中心",
    "芯片",
    "开发者",
    "云服务",
    "企业",
    "合作",
    "融资",
    "上市",
]
AI_EDUCATION_STUDENT_KEYWORDS = [
    "ai literacy",
    "future of learning",
    "students use ai",
    "students using ai",
    "student project",
    "student innovation",
    "classroom ai",
    "ai in schools",
    "ai tutor",
    "homework",
    "assessment",
    "teacher",
    "classroom",
    "school",
    "education",
    "student learning",
    "school learning",
    "learning outcomes",
    "学生",
    "课堂",
    "学校",
    "学习",
    "作业",
    "测评",
    "教师",
    "AI素养",
    "未来学习",
]
LEARNING_PSYCHOLOGY_FAMILY_TAGS = {
    "学习习惯",
    "学习方法",
    "学习动机",
    "自我管理",
    "注意力",
    "执行功能",
    "元认知",
    "考试压力",
    "考试焦虑",
    "青少年心理健康",
    "心理健康",
    "抑郁",
    "焦虑",
    "自伤预防",
    "校园压力",
    "亲子关系",
    "家庭教育",
    "屏幕时间",
    "手机成瘾",
    "睡眠",
    "运动与学习",
    "脑科学",
    "认知科学",
    "学习科学",
    "学习科学研究",
    "社交情绪学习",
    "SEL",
    "青春期",
    "压力管理",
    "心理韧性",
    "阅读兴趣",
    "数学焦虑",
}
LEARNING_PSYCHOLOGY_CONTEXT_KEYWORDS = [
    "student",
    "students",
    "school",
    "schools",
    "teacher",
    "teachers",
    "classroom",
    "homework",
    "parents",
    "parent",
    "family",
    "families",
    "children",
    "kids",
    "teen",
    "teens",
    "adolescent",
    "adolescents",
    "youth",
    "learning",
    "academic",
    "exam",
    "test",
    "学生",
    "学校",
    "课堂",
    "老师",
    "教师",
    "作业",
    "家长",
    "父母",
    "家庭",
    "孩子",
    "儿童",
    "青少年",
    "青春期",
    "学习",
    "学业",
    "考试",
    "校园",
    "亲子",
]
GENERIC_PSYCHOLOGY_TAGS = {"心理健康", "抑郁", "焦虑", "压力管理", "心理韧性"}
GENERIC_PSYCHOLOGY_KEYWORDS = [
    "mental health",
    "depression",
    "anxiety",
    "stress management",
    "resilience",
    "心理健康",
    "抑郁",
    "焦虑",
    "压力管理",
    "心理韧性",
]
LEARNING_PSYCHOLOGY_FAMILY_KEYWORDS = [
    "study habits",
    "learning habits",
    "learning motivation",
    "self-regulation",
    "executive function",
    "attention",
    "metacognition",
    "test anxiety",
    "exam stress",
    "academic pressure",
    "student stress",
    "youth mental health",
    "teen mental health",
    "adolescent mental health",
    "depression",
    "anxiety",
    "self-harm prevention",
    "suicide prevention",
    "school pressure",
    "parent-child relationship",
    "screen time",
    "sleep and learning",
    "exercise and learning",
    "brain science",
    "cognitive science",
    "learning science",
    "social emotional learning",
    "adolescent brain",
    "math anxiety",
    "reading motivation",
    "学习习惯",
    "学习方法",
    "学习动机",
    "自我管理",
    "执行功能",
    "注意力",
    "元认知",
    "考试压力",
    "考试焦虑",
    "学业压力",
    "青少年心理健康",
    "抑郁",
    "焦虑",
    "自伤",
    "自杀预防",
    "校园压力",
    "学生心理危机",
    "亲子关系",
    "亲子冲突",
    "屏幕时间",
    "手机成瘾",
    "睡眠",
    "睡眠不足",
    "运动与学习",
    "脑科学",
    "认知科学",
    "社交情绪学习",
    "青春期",
    "厌学",
    "生命教育",
    "压力管理",
    "心理韧性",
    "阅读兴趣",
    "数学焦虑",
]
SUBJECT_LEARNING_TAGS = {"阅读", "阅读教育", "数学", "数学学习", "英语学习", "英语输入", "STEM资源", "科学/STEM"}
SUBJECT_LEARNING_KEYWORDS = [
    "reading",
    "literacy",
    "writing",
    "math",
    "mathematics",
    "english learning",
    "vocabulary",
    "grammar",
    "stem",
    "science learning",
    "阅读",
    "写作",
    "数学",
    "英语",
    "词汇",
    "语法",
    "科学学习",
]
LOW_QUALITY_PSYCHOLOGY_NOISE_KEYWORDS = [
    "secret trick",
    "one simple trick",
    "miracle",
    "cure anxiety",
    "limited-time",
    "bootcamp",
    "course sale",
    "consultation",
    "sign up",
    "coaching package",
    "标题党",
    "焦虑营销",
    "限时优惠",
    "训练营",
    "课程销售",
    "心理咨询套餐",
    "报名咨询",
    "逆袭",
    "鸡娃",
]
RESOURCE_POSITIVE_TAGS = {
    "七爸干货资源",
    "免费学习资源",
    "AI认知资源",
    "数学学习资源",
    "英语学习资源",
    "STEM资源",
    "阅读写作资源",
    "互动学习游戏",
    "题库/挑战资源",
    "公开课程",
    "权威教育资源",
    "中文学习资源",
    "繁体中文教育资源",
}
RESOURCE_NOISE_TAGS = {"教培广告", "课程销售", "留资引流", "普通科技工具", "企业培训", "纯营销发布"}
RESOURCE_INTENT_KEYWORDS = [
    "free learning resources",
    "public learning resource",
    "open educational resource",
    "interactive learning game",
    "interactive ai game",
    "ai literacy game",
    "ai literacy resource",
    "student toolkit",
    "teacher toolkit",
    "curriculum resource",
    "worksheet",
    "worksheets",
    "problem bank",
    "challenge problems",
    "problem set",
    "olympiad problem set",
    "english reading resource",
    "graded reading materials",
    "vocabulary practice",
    "open course",
    "museum education resource",
    "university learning resource",
    "learning activity",
    "science activity",
    "engineering challenge",
    "学习资源",
    "免费学习资源",
    "公開學習資源",
    "公开课",
    "题库",
    "題庫",
    "挑战",
    "挑戰",
    "AI启蒙",
    "人工智能素养",
    "英语分级阅读",
    "英文閱讀",
    "数学挑战",
    "數學挑戰",
    "博物馆教育资源",
]
RESOURCE_LEARNING_CONTEXT_KEYWORDS = [
    "student",
    "students",
    "children",
    "kids",
    "teen",
    "aged",
    "k-12",
    "middle school",
    "high school",
    "teacher",
    "classroom",
    "curriculum",
    "learning",
    "education",
    "practice",
    "problem solving",
    "esl",
    "efl",
    "学生",
    "孩子",
    "儿童",
    "青少年",
    "中小学",
    "教师",
    "课堂",
    "课程",
    "学习",
    "练习",
    "閱讀",
]
RESOURCE_HARD_NOISE_KEYWORDS = [
    "limited-time paid",
    "paid bootcamp",
    "bootcamp",
    "sign up for a consultation",
    "book a consultation",
    "request a sales demo",
    "leave your phone number",
    "enterprise workflow automation",
    "productivity platform",
    "developer productivity tool",
    "office automation tool",
    "enterprise training",
    "corporate learning platform",
    "sponsored",
    "marketing campaign",
    "训练营",
    "限时报名",
    "预约咨询",
    "添加顾问",
    "加微信",
    "留资",
    "企业工作流",
    "办公效率工具",
    "开发者效率工具",
    "企业培训",
    "营销活动",
]
RESOURCE_CREDIBLE_KEYWORDS = [
    "university",
    "mit",
    "stanford",
    "harvard",
    "google",
    "microsoft",
    "openai",
    "museum",
    "library",
    "official",
    "nonprofit",
    "foundation",
    "公益",
    "官方",
    "大学",
    "博物馆",
    "图书馆",
    "教育机构",
]
RESOURCE_RECENT_KEYWORDS = [
    "new",
    "launch",
    "launched",
    "introduces",
    "updated",
    "recently",
    "newly",
    "2026",
    "2025",
    "新上线",
    "发布",
    "推出",
    "近期更新",
    "近期被讨论",
    "最近",
]
RESOURCE_CLASSIC_KEYWORDS = ["classic", "many years ago", "old", "archive", "经典资源", "多年未更新", "很久以前"]
SEASONAL_CALENDAR = {
    "late_may_june": {
        "ranges": [("05-20", "06-30")],
        "topics": [
            "期末考试",
            "期末复习",
            "考试焦虑",
            "错题整理",
            "暑假规划",
            "暑假阅读",
            "暑假书单",
            "自主阅读",
            "阅读兴趣",
            "亲子阅读",
            "夏令营选择",
            "儿童运动",
            "夏季运动",
            "游泳安全",
            "亲子游准备",
            "博物馆教育",
            "主题乐园",
            "迪士尼",
            "美食营",
            "食育",
        ],
    },
    "july_august": {
        "ranges": [("07-01", "08-20")],
        "topics": [
            "暑假执行",
            "阅读",
            "数学保持",
            "英语输入",
            "暑假作业",
            "屏幕时间",
            "夏季运动",
            "游泳安全",
            "户外活动",
            "近视防控",
            "旅行学习",
            "亲子游",
            "迪士尼",
            "主题乐园",
            "博物馆教育",
            "科技馆",
            "夏令营",
            "食育",
            "美食营",
            "生活技能",
        ],
    },
    "late_august_september": {
        "ranges": [("08-21", "09-30")],
        "topics": ["开学准备", "收心", "学习习惯", "作业补完", "新学期适应", "班级关系", "运动恢复"],
    },
    "october": {
        "ranges": [("10-01", "10-31")],
        "topics": ["国庆亲子游", "博物馆", "户外活动", "项目学习", "秋季阅读", "运动习惯"],
    },
    "november_december": {
        "ranges": [("11-01", "12-31")],
        "topics": ["期中考试", "期末复习", "错题整理", "考试压力", "睡眠", "冬季运动", "年度总结", "寒假计划"],
    },
    "january_february": {
        "ranges": [("01-01", "02-28"), ("02-29", "02-29")],
        "topics": ["寒假计划", "寒假阅读", "春节亲子关系", "压岁钱教育", "屏幕时间", "旅行", "生活技能"],
    },
    "march_april": {
        "ranges": [("03-01", "04-30")],
        "topics": ["新学期习惯", "春游", "运动", "阅读节", "期中准备", "科学教育", "户外活动"],
    },
}
SEASONAL_TOPIC_KEYWORDS = {
    "期末考试": ["final exams", "end-of-term", "期末考试", "期末"],
    "期末复习": ["exam preparation", "review plan", "期末复习", "复习计划", "考前复习"],
    "考试焦虑": ["test anxiety", "exam stress", "考试焦虑", "考试压力", "考前压力"],
    "错题整理": ["mistake notebook", "错题整理", "错题本", "错题"],
    "暑假规划": ["summer plan", "summer planning", "暑假规划", "暑假计划", "暑假作息"],
    "暑假阅读": ["summer reading", "暑假阅读", "暑期阅读"],
    "暑假书单": ["summer book list", "required reading", "暑假书单", "学校指定阅读", "名著书单"],
    "自主阅读": ["independent reading", "reading choice", "student choice", "自主阅读", "孩子自主选书"],
    "阅读兴趣": ["reading interest", "love of reading", "阅读兴趣", "不读书"],
    "亲子阅读": ["family reading", "read with children", "亲子阅读"],
    "夏令营选择": ["summer camp choice", "choose summer camp", "夏令营选择", "营地选择"],
    "儿童运动": ["children's sports", "children sports", "儿童运动", "孩子运动"],
    "夏季运动": ["summer sports", "summer exercise", "夏季运动", "暑期运动"],
    "游泳安全": ["swimming safety", "water safety", "游泳安全", "防溺水"],
    "亲子游准备": ["family travel preparation", "summer travel preparation", "亲子游准备", "暑假旅行准备"],
    "博物馆教育": ["museum education", "museum visits", "博物馆教育", "博物馆"],
    "主题乐园": ["theme park", "主题乐园"],
    "迪士尼": ["Disney", "迪士尼"],
    "美食营": ["cooking camp", "food camp", "美食营", "烹饪营"],
    "食育": ["food education", "nutrition education", "食育", "营养"],
    "暑假执行": ["summer routine", "summer schedule", "暑假执行", "暑假作息"],
    "阅读": ["reading habit", "reading", "阅读"],
    "数学保持": ["math practice", "math maintenance", "数学保持", "数学练习"],
    "英语输入": ["English input", "English reading", "English listening", "英语输入", "英语听力", "英文阅读"],
    "暑假作业": ["summer homework", "暑假作业"],
    "屏幕时间": ["screen time", "屏幕时间"],
    "户外活动": ["outdoor activities", "outdoor activity", "户外活动"],
    "近视防控": ["myopia prevention", "vision health", "近视防控", "视力保护"],
    "旅行学习": ["learning during summer trips", "travel learning", "旅行学习", "旅行中的学习"],
    "亲子游": ["family travel", "family trip", "亲子游", "暑假旅行"],
    "科技馆": ["science museum", "科技馆"],
    "夏令营": ["summer camp", "camp education", "夏令营", "营地教育"],
    "生活技能": ["life skills", "chores", "生活技能", "家务", "劳动教育"],
    "开学准备": ["back to school", "school preparation", "开学准备"],
    "收心": ["back-to-school routine", "收心"],
    "学习习惯": ["learning habits", "study habits", "学习习惯"],
    "作业补完": ["finish homework", "作业补完", "补作业"],
    "新学期适应": ["new semester adjustment", "新学期适应"],
    "班级关系": ["classroom relationships", "peer relationships", "班级关系", "同伴关系"],
    "运动恢复": ["exercise routine", "运动恢复"],
    "国庆亲子游": ["national day family travel", "国庆亲子游"],
    "博物馆": ["museum", "博物馆"],
    "项目学习": ["project-based learning", "project learning", "项目学习"],
    "秋季阅读": ["fall reading", "autumn reading", "秋季阅读"],
    "运动习惯": ["sports habits", "exercise habits", "运动习惯"],
    "期中考试": ["midterm exams", "期中考试"],
    "考试压力": ["exam pressure", "考试压力"],
    "睡眠": ["sleep", "睡眠"],
    "冬季运动": ["winter sports", "冬季运动"],
    "年度总结": ["year-end reflection", "年度总结"],
    "寒假计划": ["winter holiday plan", "寒假计划"],
    "寒假阅读": ["winter holiday reading", "寒假阅读"],
    "春节亲子关系": ["spring festival parenting", "春节亲子关系", "春节亲子"],
    "压岁钱教育": ["money education", "lucky money", "压岁钱教育", "压岁钱"],
    "旅行": ["travel with children", "旅行"],
    "新学期习惯": ["new semester habits", "新学期习惯"],
    "春游": ["spring outing", "春游"],
    "运动": ["sports", "exercise", "运动"],
    "阅读节": ["reading festival", "阅读节"],
    "期中准备": ["midterm preparation", "期中准备"],
    "科学教育": ["science education", "科学教育"],
}
SEASONAL_PARENT_CHILD_KEYWORDS = [
    "parents",
    "parent support",
    "families",
    "family",
    "children",
    "students",
    "kids",
    "k-12",
    "elementary",
    "middle school",
    "school",
    "家长",
    "父母",
    "家庭",
    "孩子",
    "儿童",
    "学生",
    "中小学",
    "小学",
    "初中",
    "学校",
    "亲子",
]
SEASONAL_DECISION_KEYWORDS = [
    "plan",
    "planning",
    "guide",
    "how parents can",
    "choose",
    "choice",
    "schedule",
    "routine",
    "support",
    "prepare",
    "preparation",
    "计划",
    "规划",
    "指南",
    "选择",
    "安排",
    "作息",
    "支持",
    "准备",
    "避坑",
]
SEASONAL_GROWTH_KEYWORDS = [
    "reading",
    "sports",
    "exercise",
    "independence",
    "life skills",
    "curiosity",
    "learning",
    "creativity",
    "mental health",
    "sleep",
    "阅读",
    "运动",
    "独立性",
    "生活技能",
    "好奇心",
    "学习能力",
    "创造力",
    "心理健康",
    "睡眠",
]
SEASONAL_WRITABLE_KEYWORDS = [
    "reflects",
    "discusses",
    "explains",
    "how",
    "guide",
    "why",
    "tips",
    "方法",
    "反思",
    "讨论",
    "解释",
    "为什么",
    "怎么",
    "建议",
]
SEASONAL_RISK_KEYWORDS = [
    "limited-time discount",
    "enrollment discount",
    "sign-up bonus",
    "consultation form",
    "hotel packages",
    "shopping discounts",
    "luxury resorts",
    "ticket prices",
    "fast pass rules",
    "expired promotion",
    "paid summer camp packages",
    "training company",
    "招生",
    "报名优惠",
    "限时优惠",
    "留资",
    "咨询表",
    "教培",
    "酒店套餐",
    "购物折扣",
    "奢华度假村",
    "票价",
    "过期促销",
    "纯营销",
]
SEASONAL_HARD_NOISE_KEYWORDS = [
    "limited-time summer camp enrollment discount",
    "paid summer camp packages",
    "consultation forms",
    "sign-up bonuses",
    "top luxury resorts",
    "hotel packages",
    "shopping discounts",
    "ticket prices and fast pass rules from 2017",
    "outdated ticket prices",
    "expired promotion details",
    "medical treatment",
    "diagnosis",
    "medicine dosage",
    "夏令营招生",
    "课程招生",
    "旅游软文",
    "过时票价",
    "过时政策",
    "过期活动",
    "用药",
    "诊断",
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


def learning_resource_can_enter_top20(item: dict) -> bool:
    if item.get("source_category") != "learning_resource":
        return True
    score = int(item.get("priority_score") or 0)
    tags = item.get("tags", [])
    tag_set = set(tags)
    text = item_text(item, tags)
    pitch = item.get("qiba_pitch", "")
    resource_score = score_learning_resource(item, tags, text)
    if is_learning_resource_candidate(item, tags, text) and resource_score >= RESOURCE_MIN_SCORE:
        return True
    if score >= 75 and has_any(pitch, ["适合写成主稿", "适合七点半爸爸主稿", "可以转化为七爸选题", "七爸选题"]):
        return True
    return score >= 65 and bool(tag_set & LEARNING_RESOURCE_MAJOR_TOP_PICK_TAGS)


def has_qiba_signal(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return bool(set(tags) & (FIT_TAGS | HIGH_VALUE_EDUCATION_TAGS)) or has_any(
        text,
        ["education", "learning", "student", "school", "children", "teen", "parent", "family", "screen time", "media literacy", "ai tutor"],
    )


def is_enterprise_only(title: str, summary: str, tags: list[str]) -> bool:
    text = f"{title} {summary}"
    return has_any(text, ENTERPRISE_ONLY_KEYWORDS) and not has_qiba_signal(title, summary, tags)


def is_ai_education_or_student_case(item: dict) -> bool:
    tags = set(item.get("tags", []))
    text = item_text(item, item.get("tags", []))
    if tags & {"AI教育", "AI时代学生画像", "学生Builder", "未来学习", "项目制学习"}:
        return True
    return has_any(text, AI_STUDENT_TECH_SIGNALS) and has_any(text, AI_EDUCATION_STUDENT_KEYWORDS)


def is_pure_ai_tech_news(item: dict) -> bool:
    tags = set(item.get("tags", []))
    text = item_text(item, item.get("tags", []))
    source = item.get("source", "")
    has_ai_or_tech = source in TECH_NEWS_SOURCES or bool(tags & {"AI", "高科技", "科技巨头", "OpenAI", "Google", "Microsoft", "Meta", "Apple", "NVIDIA"}) or has_any(text, AI_KEYWORDS + ["anthropic", "mistral", "spacex", "gemini"])
    if not has_ai_or_tech:
        return False
    if is_ai_education_or_student_case(item):
        return False
    if has_any(text, GENERAL_TECH_EDUCATION_TRANSLATION_SIGNALS) and not has_any(text, PURE_AI_TECH_KEYWORDS):
        return False
    return source in TECH_NEWS_SOURCES or has_any(text, PURE_AI_TECH_KEYWORDS) or bool(tags & {"高科技", "科技巨头", "OpenAI", "Google", "Microsoft", "Meta", "Apple", "NVIDIA"})


def is_low_quality_psychology_noise(item: dict) -> bool:
    text = item_text(item, item.get("tags", []))
    return has_any(text, LOW_QUALITY_PSYCHOLOGY_NOISE_KEYWORDS) or bool(set(item.get("tags", [])) & {"教培广告", "课程销售", "留资引流", "纯营销发布"})


def is_learning_psychology_family(item: dict) -> bool:
    tags = set(item.get("tags", []))
    text = item_text(item, item.get("tags", []))
    plain_text = f"{item.get('title', '')} {item.get('summary', '')}"
    if is_low_quality_psychology_noise(item):
        return False
    has_context = has_any(plain_text, LEARNING_PSYCHOLOGY_CONTEXT_KEYWORDS)
    specific_tags = tags & (LEARNING_PSYCHOLOGY_FAMILY_TAGS - GENERIC_PSYCHOLOGY_TAGS)
    if specific_tags:
        return True
    if tags & GENERIC_PSYCHOLOGY_TAGS:
        return has_context
    if has_any(text, GENERIC_PSYCHOLOGY_KEYWORDS) and not has_context:
        return False
    return has_any(text, LEARNING_PSYCHOLOGY_FAMILY_KEYWORDS) and has_context


def classify_topic_family(item: dict) -> str:
    tags = set(item.get("tags", []))
    text = item_text(item, item.get("tags", []))
    if is_ai_education_or_student_case(item):
        return "ai_education_student"
    if is_pure_ai_tech_news(item):
        return "pure_ai_tech"
    if is_learning_psychology_family(item):
        return "learning_psychology_family"
    if bool(tags & SUBJECT_LEARNING_TAGS) or has_any(text, SUBJECT_LEARNING_KEYWORDS):
        return "subject_learning"
    if bool(tags & {"教育研究", "儿童与青少年", "美国高校", "教育热点"}) or has_any(text, ["education policy", "school district", "education research", "public school", "naep", "教育政策", "学校制度", "教育研究"]):
        return "education_policy_research"
    return "other"


def apply_topic_family_score_adjustment(item: dict) -> int:
    family = classify_topic_family(item)
    text = item_text(item, item.get("tags", []))
    if is_low_quality_psychology_noise(item):
        return -25
    if family == "learning_psychology_family":
        bonus = 12
        if has_any(text, ["study", "research", "report", "guidance", "guide", "public health", "academy", "university", "研究", "报告", "指南", "大学", "公共卫生"]):
            bonus += 4
        return bonus
    if family == "ai_education_student":
        bonus = 4
        if has_any(text, ["classroom", "students use", "student project", "teacher", "homework", "assessment", "课堂", "学生使用", "学生项目", "作业", "测评"]):
            bonus += 4
        return bonus
    if family == "subject_learning":
        return 5
    if family == "education_policy_research":
        return 2
    if family == "pure_ai_tech":
        penalty = -12
        if has_any(text, PURE_AI_TECH_KEYWORDS):
            penalty -= 8
        return penalty
    return 0


def calculate_priority_score(item: dict, tags: list[str], now: datetime) -> int:
    title = clean_text(item.get("title", ""))
    summary = clean_text(item.get("summary", ""))
    scoring_item = dict(item)
    scoring_item["tags"] = tags
    text = f"{title} {summary} {' '.join(tags)}"
    score = (
        source_priority(item.get("source", ""))
        + theme_priority(title, summary, tags)
        + qiba_fit_priority(title, summary, tags)
        + recency_priority(item.get("published_at", ""), now)
        - downrank_penalty(title, summary)
        - education_media_penalty(item, tags)
        + ai_student_builder_bonus(item, tags, text)
        + apply_topic_family_score_adjustment(scoring_item)
    )
    if is_low_quality_psychology_noise(scoring_item):
        score = min(score, 45)
    if classify_topic_family(scoring_item) == "pure_ai_tech":
        score = min(score, 62)
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


def repeat_fallback_age_days(item: dict, current_date: date | datetime | str | None) -> int | None:
    first_seen = item.get("first_seen_date", "")
    if not first_seen:
        return None
    try:
        first_seen_date = date.fromisoformat(first_seen[:10])
    except ValueError:
        return None
    if current_date is not None:
        reference_date = coerce_report_date(current_date)
    else:
        published = parse_published_at(item.get("published_at", ""))
        reference_date = published.astimezone(REPORT_TZ).date() if published else datetime.now(REPORT_TZ).date()
    return (reference_date - first_seen_date).days


def duplicate_reason_value(item: dict) -> str:
    reason = item.get("duplicate_reason", "")
    first_seen = item.get("first_seen_date", "")
    return f"duplicate:{reason}:{first_seen}" if first_seen else f"duplicate:{reason}"


def has_repeat_fallback_hard_noise(item: dict) -> bool:
    tags = item.get("tags", [])
    text = item_text(item, tags)
    return bool(set(tags) & RESOURCE_NOISE_TAGS) or has_any(
        text,
        RESOURCE_HARD_NOISE_KEYWORDS
        + SEASONAL_HARD_NOISE_KEYWORDS
        + [
            "marketing",
            "sponsored",
            "press release",
            "limited-time discount",
            "sign up",
            "consultation",
            "enrollment discount",
            "hotel package",
            "shopping discount",
            "招生",
            "留资",
            "促销",
            "团购",
        ],
    )


def repeat_fallback_tag_bonus(item: dict) -> int:
    tags = set(item.get("tags", []))
    bonus = min(len(tags & REPEAT_FALLBACK_HIGH_VALUE_TAGS) * 8, 32)
    family = classify_topic_family(item)
    if family == "learning_psychology_family":
        bonus += 16
    elif family == "subject_learning":
        bonus += 8
    elif family == "pure_ai_tech":
        bonus -= 20
    if item.get("source") in REPEAT_FALLBACK_PREFERRED_SOURCES:
        bonus += 8
    reason = item.get("duplicate_reason", "")
    if reason in {"same_title", "similar_title"}:
        bonus += 6
    return bonus


def can_use_repeat_fallback(item: dict, current_date: date | datetime | str | None = None) -> bool:
    if not item.get("is_duplicate"):
        return False
    if item.get("is_evergreen_fallback") or item.get("topic_type") == "seasonal_evergreen_fallback":
        return False
    reason = item.get("duplicate_reason", "")
    if reason not in {"same_link", "same_title", "similar_title"}:
        return False
    score = int(item.get("priority_score") or 0)
    tags = set(item.get("tags", []))
    has_high_value_tag = bool(tags & REPEAT_FALLBACK_HIGH_VALUE_TAGS)
    if score < REPEAT_FALLBACK_MIN_SCORE and not (score >= REPEAT_FALLBACK_TAG_MIN_SCORE and has_high_value_tag):
        return False
    if reason == "same_link":
        age_days = repeat_fallback_age_days(item, current_date)
        if age_days is not None and age_days <= 1:
            return False
    if has_repeat_fallback_hard_noise(item):
        return False
    if classify_topic_family(item) == "pure_ai_tech" and score < 75:
        return False
    if not general_tech_reserve_can_enter_top20(item):
        return False
    if not supplemental_education_media_can_enter_top20(item):
        return False
    if not learning_resource_can_enter_top20(item):
        return False
    title = item.get("title", "")
    summary = item.get("summary", "")
    return has_qiba_signal(title, summary, item.get("tags", [])) or has_high_value_tag


def repeat_fallback_sort_key(item: dict, current_date: date | datetime | str | None = None) -> tuple[int, int, int, int, int, str]:
    reason_priority = {"same_title": 3, "similar_title": 2, "same_link": 1}.get(item.get("duplicate_reason", ""), 0)
    age_days = repeat_fallback_age_days(item, current_date)
    age_value = age_days if age_days is not None else 0
    source_value = 1 if item.get("source") in REPEAT_FALLBACK_PREFERRED_SOURCES else 0
    return (
        int(item.get("priority_score") or 0),
        repeat_fallback_tag_bonus(item),
        reason_priority,
        age_value,
        source_value,
        item.get("published_at", ""),
    )


def repeat_fallback_source_limit(source: str) -> int:
    if source in REPEAT_FALLBACK_PREFERRED_SOURCES:
        return MAX_TOP_PICKS_PER_SOURCE + 1
    return MAX_TOP_PICKS_PER_SOURCE


def is_ai_tech_family(family: str) -> bool:
    return family in {"pure_ai_tech", "ai_education_student"}


def has_high_quality_topic_override(item: dict) -> bool:
    family = classify_topic_family(item)
    score = int(item.get("priority_score") or 0)
    if family == "learning_psychology_family" and score >= 48:
        return True
    if family == "ai_education_student" and score >= 78:
        return True
    if family == "subject_learning" and score >= 55:
        return True
    return score >= 82 and has_qiba_signal(item.get("title", ""), item.get("summary", ""), item.get("tags", []))


def top20_candidate_quality_ok(item: dict) -> bool:
    if is_low_quality_psychology_noise(item):
        return False
    if not general_tech_reserve_can_enter_top20(item):
        return False
    if not supplemental_education_media_can_enter_top20(item):
        return False
    if not learning_resource_can_enter_top20(item):
        return False
    source = item.get("source", "")
    if source in BROAD_WELLBEING_RESEARCH_SOURCES:
        plain_text = f"{item.get('title', '')} {item.get('summary', '')}"
        if not has_any(plain_text, BROAD_WELLBEING_STRONG_CONTEXT_KEYWORDS):
            return False
        if has_any(plain_text, BROAD_WELLBEING_MEDICAL_NOISE_KEYWORDS) and not has_any(
            plain_text,
            ["child", "children", "kid", "kids", "teen", "teens", "adolescent", "adolescents", "youth", "student", "students", "孩子", "儿童", "青少年", "学生"],
        ):
            return False
    return True


def can_select_with_topic_balance(
    item: dict,
    selected: list[dict],
    source_counts: dict[str, int],
    supplemental_education_media_count: int,
    strict: bool = True,
    enforce_soft_caps: bool = True,
) -> bool:
    source = item.get("source", "")
    score = int(item.get("priority_score") or 0)
    family = classify_topic_family(item)
    is_high_score = score >= 80
    if not top20_candidate_quality_ok(item):
        return False
    if family == "pure_ai_tech" and score < 35:
        return False
    if family == "ai_education_student" and score < 30:
        return False
    if family == "learning_psychology_family" and score < 35:
        return False
    if family == "subject_learning" and score < 28:
        return False
    if family == "education_policy_research" and score < 35:
        return False
    if family == "other" and score < 30:
        return False
    source_limit = MAX_TOP_PICKS_PER_SOURCE
    if is_high_score and source not in BROAD_WELLBEING_RESEARCH_SOURCES:
        source_limit += 1
    if source_counts.get(source, 0) >= source_limit:
        return False
    if (
        not is_high_score
        and source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES
        and supplemental_education_media_count >= MAX_SUPPLEMENTAL_EDUCATION_MEDIA_TOP_PICKS
    ):
        return False
    if enforce_soft_caps and family == "pure_ai_tech":
        pure_count = sum(1 for selected_item in selected if classify_topic_family(selected_item) == "pure_ai_tech")
        if pure_count >= PURE_AI_TECH_SOFT_CAP:
            return False
    if enforce_soft_caps and is_ai_tech_family(family):
        ai_count = sum(1 for selected_item in selected if is_ai_tech_family(classify_topic_family(selected_item)))
        if ai_count >= AI_TECH_SOFT_CAP and not (score >= 82 and family == "ai_education_student"):
            return False
    if not strict:
        if family == "pure_ai_tech" and score < 50:
            return False
        if family == "other" and score < 30:
            return False
        return score >= TOPIC_FAMILY_RELAXED_MIN_SCORE or has_high_quality_topic_override(item)
    return True


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
        resources_file = data_dir / f"{date_text}_resources.json"
        resources_md_file = data_dir / f"{date_text}_resources.md"
        if resources_file.exists():
            try:
                resources = json.loads(resources_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                resources = []
            entry["resourcesFile"] = f"data/{date_text}_resources.json"
            entry["resourcesMarkdownFile"] = f"data/{date_text}_resources.md"
            entry["resourceCount"] = len(resources)
        elif resources_md_file.exists():
            entry["resourcesMarkdownFile"] = f"data/{date_text}_resources.md"
            entry["resourceCount"] = 0
        seasonal_file = data_dir / f"{date_text}_seasonal.json"
        seasonal_md_file = data_dir / f"{date_text}_seasonal.md"
        if seasonal_file.exists():
            try:
                seasonal_items = json.loads(seasonal_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                seasonal_items = []
            entry["seasonalFile"] = f"data/{date_text}_seasonal.json"
            entry["seasonalMarkdownFile"] = f"data/{date_text}_seasonal.md"
            entry["seasonalCount"] = len(seasonal_items)
        elif seasonal_md_file.exists():
            entry["seasonalMarkdownFile"] = f"data/{date_text}_seasonal.md"
            entry["seasonalCount"] = 0
        if total_count is not None:
            entry["totalCount"] = total_count
        if duplicate_count is not None:
            entry["duplicateCount"] = duplicate_count
        archive_index.append(entry)

    archive_index.sort(key=lambda entry: entry["date"], reverse=True)
    archive_data = {entry["date"]: archive_data[entry["date"]] for entry in archive_index}
    return archive_index, archive_data


def select_top_picks(
    items: list[dict],
    limit: int = TOP_PICK_LIMIT,
    current_date: date | datetime | str | None = None,
) -> list[dict]:
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
    selected_links: set[str] = set()

    learning_candidates = [
        item
        for item in ranked
        if classify_topic_family(item) == "learning_psychology_family"
        and int(item.get("priority_score") or 0) >= 45
        and top20_candidate_quality_ok(item)
    ]
    for item in learning_candidates:
        learning_count = sum(1 for selected_item in selected if classify_topic_family(selected_item) == "learning_psychology_family")
        if learning_count >= LEARNING_PSYCH_FAMILY_TARGET:
            break
        if item.get("link") in selected_links:
            continue
        if not can_select_with_topic_balance(item, selected, source_counts, supplemental_education_media_count, strict=True):
            continue
        source = item.get("source", "")
        selected.append(item)
        selected_links.add(item.get("link"))
        source_counts[source] = source_counts.get(source, 0) + 1
        if source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
            supplemental_education_media_count += 1
        if len(selected) == limit:
            return selected

    for item in ranked:
        if item.get("link") in selected_links:
            continue
        if not can_select_with_topic_balance(item, selected, source_counts, supplemental_education_media_count, strict=True):
            continue
        source = item.get("source", "")
        selected.append(item)
        selected_links.add(item.get("link"))
        source_counts[source] = source_counts.get(source, 0) + 1
        if source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
            supplemental_education_media_count += 1
        if len(selected) == limit:
            return selected

    if len(selected) < limit:
        for item in ranked:
            if item.get("link") in selected_links:
                continue
            if not can_select_with_topic_balance(
                item,
                selected,
                source_counts,
                supplemental_education_media_count,
                strict=False,
                enforce_soft_caps=False,
            ):
                continue
            source = item.get("source", "")
            selected.append(item)
            selected_links.add(item.get("link"))
            source_counts[source] = source_counts.get(source, 0) + 1
            if source in SUPPLEMENTAL_EDUCATION_MEDIA_SOURCES:
                supplemental_education_media_count += 1
            if len(selected) == limit:
                return selected

    if len(selected) < limit:
        repeat_candidates = [
            item
            for item in items
            if item.get("link")
            and item.get("link") not in selected_links
            and can_use_repeat_fallback(item, current_date)
        ]
        repeat_candidates.sort(key=lambda item: repeat_fallback_sort_key(item, current_date), reverse=True)
        for item in repeat_candidates:
            source = item.get("source", "")
            if not can_select_with_topic_balance(
                item,
                selected,
                source_counts,
                supplemental_education_media_count,
                strict=True,
                enforce_soft_caps=False,
            ):
                continue
            if source_counts.get(source, 0) >= repeat_fallback_source_limit(source):
                continue
            fallback_item = dict(item)
            fallback_item["is_repeat_fallback"] = True
            fallback_item["allow_repeat"] = True
            fallback_item["repeat_reason"] = duplicate_reason_value(item)
            fallback_item["top20_fill_reason"] = "主榜非重复候选不足20，作为高价值历史候选补位"
            selected.append(fallback_item)
            selected_links.add(fallback_item.get("link"))
            source_counts[source] = source_counts.get(source, 0) + 1
            if len(selected) == limit:
                return selected
    return selected


def item_text(item: dict, tags: list[str]) -> str:
    return f"{item.get('title', '')} {item.get('summary', '')} {' '.join(tags)}"


def is_recent_enough_for_resource(item: dict, text: str) -> bool:
    if has_any(text, RESOURCE_RECENT_KEYWORDS):
        return True
    published = parse_published_at(item.get("published_at", ""))
    if not published:
        return False
    now = datetime.now(timezone.utc)
    if not published.tzinfo:
        published = published.replace(tzinfo=timezone.utc)
    return (now - published.astimezone(timezone.utc)).days <= 90


def is_learning_resource_candidate(item: dict, tags: list[str], text: str) -> bool:
    tag_set = set(tags)
    if tag_set & RESOURCE_NOISE_TAGS:
        return False
    if has_any(text, RESOURCE_HARD_NOISE_KEYWORDS):
        return False
    if has_any(text, ["copyright", "pirated", "网盘", "盗版"]):
        return False
    has_resource_intent = bool(tag_set & RESOURCE_POSITIVE_TAGS) or has_any(text, RESOURCE_INTENT_KEYWORDS)
    has_learning_context = has_any(text, RESOURCE_LEARNING_CONTEXT_KEYWORDS)
    if not (has_resource_intent and has_learning_context):
        return False
    if has_any(text, RESOURCE_CLASSIC_KEYWORDS) and not has_any(text, ["recently discussed", "recently rediscovered", "近期被讨论", "近期再发现"]):
        return False
    if not is_recent_enough_for_resource(item, text):
        return False
    if has_any(text, ["enterprise", "workflow automation", "productivity platform", "developer tool"]) and not has_learning_context:
        return False
    return True


def classify_resource_subject(item: dict, tags: list[str], text: str) -> str:
    tag_set = set(tags)
    if "AI认知资源" in tag_set or has_any(text, ["ai literacy", "interactive ai game", "artificial intelligence", "AI启蒙", "人工智能素养"]):
        return "AI认知"
    if "数学学习资源" in tag_set or has_any(text, ["math challenge", "mathematics", "problem bank", "olympiad", "数学", "數學"]):
        return "数学学习"
    if "英语学习资源" in tag_set or has_any(text, ["english reading", "graded reading", "vocabulary practice", "esl", "efl", "英语", "英文閱讀"]):
        return "英语学习"
    if "阅读写作资源" in tag_set or has_any(text, ["reading resource", "writing worksheet", "literacy", "阅读", "写作", "語文"]):
        return "语文/阅读写作"
    if has_any(text, ["physics", "物理"]):
        return "物理"
    if has_any(text, ["chemistry", "化学", "化學"]):
        return "化学"
    if "STEM资源" in tag_set or has_any(text, ["stem", "science activity", "engineering challenge", "科学", "工程"]):
        return "科学/STEM"
    if has_any(text, ["history", "humanities", "历史", "人文"]):
        return "历史/人文"
    if has_any(text, ["debate", "speech", "辩论", "表达"]):
        return "辩论/表达"
    if has_any(text, ["sport", "fitness", "体育", "运动"]):
        return "体育/运动"
    return "综合学习"


def classify_resource_region(item: dict, tags: list[str], text: str) -> str:
    raw_text = f"{item.get('title', '')} {item.get('summary', '')} {item.get('source', '')}"
    if "繁体中文教育资源" in tags or has_any(raw_text, ["Taiwan", "Hong Kong", "Traditional Chinese", "臺灣", "香港", "繁體", "英文閱讀", "數學"]):
        return "繁体中文"
    if "中文学习资源" in tags or has_any(raw_text, ["简体中文", "中国学生", "语文", "公开课", "题库", "AI启蒙", "英语分级阅读"]):
        return "简体中文"
    return "英文世界"


def classify_resource_type(item: dict, tags: list[str], text: str) -> str:
    if "互动学习游戏" in tags or has_any(text, ["interactive game", "learning game", "simulation", "互动", "游戏"]) or (has_any(text, ["interactive"]) and has_any(text, ["game"])):
        return "互动游戏"
    if has_any(text, ["olympiad", "contest", "competition", "竞赛", "奧賽", "奥数"]):
        return "竞赛资源"
    if "题库/挑战资源" in tags or has_any(text, ["problem bank", "challenge problems", "problem set", "quiz", "题库", "挑战"]):
        return "题库"
    if "公开课程" in tags or has_any(text, ["open course", "online course", "公开课", "开放课程"]):
        return "公开课"
    if has_any(text, ["worksheet", "worksheets", "练习册", "工作纸"]):
        return "练习册"
    if has_any(text, ["reading material", "graded reading", "reading resource", "阅读材料", "分级阅读"]):
        return "阅读材料"
    if has_any(text, ["video course", "视频课程", "影片課程"]):
        return "视频课程"
    if has_any(text, ["project activity", "project-based", "项目活动", "專題活動"]):
        return "项目活动"
    if has_any(text, ["experiment", "lab activity", "实验", "實驗"]):
        return "实验活动"
    if has_any(text, ["toolkit", "工具包"]):
        return "工具包"
    if has_any(text, ["database", "repository", "资料库", "資料庫"]):
        return "资料库"
    if has_any(text, ["course", "curriculum", "课程", "課程"]):
        return "课程"
    return "资料库"


def classify_resource_freshness(item: dict, tags: list[str], text: str) -> str:
    if has_any(text, ["recently rediscovered", "classic resource recently", "经典资源近期再发现", "近期再发现"]):
        return "经典资源近期再发现"
    if has_any(text, ["recently discussed", "recent discussion", "近期被讨论"]):
        return "近期被讨论"
    if has_any(text, ["updated", "new version", "近期更新", "更新"]):
        return "近期更新"
    if has_any(text, ["new", "launch", "launched", "introduces", "新上线", "发布", "推出"]):
        return "新上线"
    if has_any(text, RESOURCE_CLASSIC_KEYWORDS):
        return "经典资源"
    return "近期更新" if is_recent_enough_for_resource(item, text) else "经典资源"


def classify_resource_age_range(item: dict, tags: list[str], text: str) -> str:
    match = re.search(r"aged?\s+(\d{1,2})\s*[–-]\s*(\d{1,2})", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}–{match.group(2)}岁"
    if has_any(text, ["k-12", "middle school", "high school", "中小学"]):
        return "中小学"
    if has_any(text, ["elementary", "primary school", "小学"]):
        return "小学"
    if has_any(text, ["teen", "middle school", "初中"]):
        return "初中"
    if has_any(text, ["high school", "高中"]):
        return "高中"
    if has_any(text, ["parent", "teacher", "教师", "家长"]):
        return "家长/教师"
    return "学生/家长"


def classify_resource_free_or_paid(item: dict, tags: list[str], text: str) -> str:
    if has_any(text, ["partial free", "freemium", "部分免费", "部分免費"]):
        return "部分免费"
    if has_any(text, ["paid", "subscription", "tuition", "付费", "收費", "收费"]):
        return "付费"
    if "免费学习资源" in tags or has_any(text, ["free", "open educational", "public learning", "免费", "免費", "公开"]):
        return "免费"
    return "未知"


def build_resource_reason(item: dict, tags: list[str], text: str) -> str:
    subject = classify_resource_subject(item, tags, text)
    resource_type = classify_resource_type(item, tags, text)
    if subject == "AI认知":
        return compact_chinese(f"这是可直接打开使用的{resource_type}，适合帮助孩子把 AI 从概念变成可体验、可讨论的学习对象。", 110)
    if subject == "数学学习":
        return compact_chinese(f"这是面向问题解决的{resource_type}，适合作为数学自学、挑战题训练或竞赛兴趣启蒙材料。", 110)
    if subject == "英语学习":
        return compact_chinese(f"这是偏实用的{resource_type}，适合中国学生做分级阅读、词汇练习或 ESL/EFL 场景下的输入训练。", 110)
    return compact_chinese(f"这是有明确学习入口的{resource_type}，适合家长或教师筛选后转给孩子做拓展学习。", 110)


def build_resource_qiba_angle(item: dict, tags: list[str], text: str) -> str:
    subject = classify_resource_subject(item, tags, text)
    if subject == "AI认知":
        return compact_chinese("七爸写法可从“孩子不是背 AI 概念，而是通过小游戏理解 AI 如何解决真实问题”切入，落到家庭 AI 启蒙。", 120)
    if subject == "数学学习":
        return compact_chinese("七爸写法可从“好题库不是刷题机器，而是训练孩子如何思考问题”切入，强调过程、复盘和自学能力。", 120)
    if subject == "英语学习":
        return compact_chinese("七爸写法可从“中国孩子学英语缺的不是 App，而是可持续阅读输入和词汇练习材料”切入。", 120)
    return compact_chinese("七爸写法可从“今天发现一个可以立刻用的学习资源”切入，说明适合谁、怎么用、不要怎么用。", 120)


def score_learning_resource(item: dict, tags: list[str], text: str) -> int:
    if not is_learning_resource_candidate(item, tags, text):
        return 0
    subject = classify_resource_subject(item, tags, text)
    freshness = classify_resource_freshness(item, tags, text)
    score = 0

    resource_shape_hits = sum(
        [
            has_any(text, RESOURCE_INTENT_KEYWORDS),
            has_any(text, ["interactive", "game", "problem", "worksheet", "course", "toolkit", "activity", "题库", "课程", "练习"]),
            has_any(text, RESOURCE_LEARNING_CONTEXT_KEYWORDS),
        ]
    )
    score += min(10 + resource_shape_hits * 5, 25)

    if item.get("source") in PRIORITY_SOURCES or has_any(text, RESOURCE_CREDIBLE_KEYWORDS) or "权威教育资源" in tags:
        score += 20
    elif item.get("source") in EDUCATION_MEDIA_SOURCES:
        score += 12
    else:
        score += 8

    if freshness == "新上线":
        score += 20
    elif freshness in {"近期更新", "近期被讨论", "经典资源近期再发现"}:
        score += 16
    else:
        score += 6

    if has_any(text, ["parent", "parents", "Chinese students", "student", "students", "teacher", "家长", "中国学生", "学生"]):
        score += 15
    else:
        score += 8

    if subject in {"AI认知", "数学学习", "英语学习"}:
        score += 10
    elif subject in {"科学/STEM", "语文/阅读写作"}:
        score += 7
    else:
        score += 5

    score += 5

    free_or_paid = classify_resource_free_or_paid(item, tags, text)
    if free_or_paid == "免费":
        score += 5
    elif free_or_paid == "部分免费":
        score += 2
    elif free_or_paid == "付费":
        score -= 18
    else:
        score += 1
    if set(tags) & RESOURCE_NOISE_TAGS or has_any(text, RESOURCE_HARD_NOISE_KEYWORDS):
        score -= 40
    return max(0, min(100, score))


def build_resource_item(item: dict) -> dict:
    tags = item.get("tags", [])
    text = item_text(item, tags)
    score = score_learning_resource(item, tags, text)
    return {
        "title": item.get("title", ""),
        "source": item.get("source", ""),
        "url": item.get("link", ""),
        "subject": classify_resource_subject(item, tags, text),
        "region": classify_resource_region(item, tags, text),
        "age_range": classify_resource_age_range(item, tags, text),
        "resource_type": classify_resource_type(item, tags, text),
        "free_or_paid": classify_resource_free_or_paid(item, tags, text),
        "freshness": classify_resource_freshness(item, tags, text),
        "why_useful": build_resource_reason(item, tags, text),
        "qiba_angle": build_resource_qiba_angle(item, tags, text),
        "score": score,
        "summary": item.get("summary", ""),
        "tags": tags,
        "published_at": item.get("published_at", ""),
        "is_resource_pick": False,
    }


def select_daily_resources(items: list[dict], limit: int = RESOURCE_PICK_LIMIT) -> list[dict]:
    candidates = []
    for item in items:
        resource = build_resource_item(item)
        if resource["score"] >= RESOURCE_MIN_SCORE:
            candidates.append(resource)
    candidates.sort(key=lambda resource: (resource["score"], resource.get("published_at", "")), reverse=True)

    selected: list[dict] = []
    selected_urls: set[str] = set()
    classic_count = 0
    for resource in candidates:
        url = resource.get("url", "")
        if url in selected_urls:
            continue
        is_classic = resource["freshness"] == "经典资源"
        if is_classic:
            continue
        if resource["freshness"] == "经典资源近期再发现":
            if classic_count >= 1:
                continue
            classic_count += 1
        resource["is_resource_pick"] = True
        selected.append(resource)
        selected_urls.add(url)
        if len(selected) == limit:
            break
    return selected


def coerce_report_date(today: date | datetime | str) -> date:
    if isinstance(today, datetime):
        return today.astimezone(REPORT_TZ).date() if today.tzinfo else today.date()
    if isinstance(today, date):
        return today
    return datetime.strptime(today, "%Y-%m-%d").date()


def month_day_in_range(month_day: str, start: str, end: str) -> bool:
    if start <= end:
        return start <= month_day <= end
    return month_day >= start or month_day <= end


def get_seasonal_window(today: date | datetime | str) -> str:
    report_day = coerce_report_date(today)
    month_day = report_day.strftime("%m-%d")
    for window, config in SEASONAL_CALENDAR.items():
        for start, end in config["ranges"]:
            if month_day_in_range(month_day, start, end):
                return window
    return ""


def get_active_seasonal_topics(today: date | datetime | str) -> list[str]:
    window = get_seasonal_window(today)
    if not window:
        return []
    return list(SEASONAL_CALENDAR[window]["topics"])


def matched_seasonal_topics(tags: list[str], text: str, today: date | datetime | str) -> list[str]:
    active_topics = get_active_seasonal_topics(today)
    tag_set = set(tags)
    matches = []
    for topic in active_topics:
        keywords = SEASONAL_TOPIC_KEYWORDS.get(topic, [topic])
        if topic in tag_set or has_any(text, keywords):
            matches.append(topic)
    return matches


def has_seasonal_hard_noise(text: str) -> bool:
    return has_any(text, SEASONAL_HARD_NOISE_KEYWORDS)


def classify_seasonal_theme(item: dict, tags: list[str], text: str, today: date | datetime | str) -> str:
    topics = matched_seasonal_topics(tags, text, today)
    if topics:
        return " / ".join(topics[:3])
    active_topics = get_active_seasonal_topics(today)
    return active_topics[0] if active_topics else "教育时令"


def score_seasonal_relevance(item: dict, tags: list[str], text: str, today: date | datetime | str) -> int:
    if not (item.get("link") or item.get("url")):
        return 0
    if has_seasonal_hard_noise(text):
        return 0
    topics = matched_seasonal_topics(tags, text, today)
    if not topics:
        return 0
    score = 0
    score += min(10 + len(topics) * 5, 25)

    if has_any(text, SEASONAL_PARENT_CHILD_KEYWORDS) or set(tags) & {"家庭教育", "亲子教育", "儿童与青少年", "K12教育"}:
        score += 20
    else:
        score += 8

    if has_any(text, SEASONAL_DECISION_KEYWORDS):
        score += 15
    else:
        score += 5

    if has_any(text, SEASONAL_GROWTH_KEYWORDS) or set(tags) & {"阅读", "数学", "屏幕时间", "心理健康", "学习能力"}:
        score += 15
    else:
        score += 6

    if has_any(text, SEASONAL_WRITABLE_KEYWORDS) or item.get("priority_score", 0) >= 55:
        score += 15
    else:
        score += 7

    if has_any(text, ["Chinese families", "parents", "families", "家长", "中国家庭", "亲子"]):
        score += 5
    else:
        score += 2

    if has_any(text, SEASONAL_RISK_KEYWORDS):
        score -= 35
    if has_any(text, ["2017", "2018", "outdated", "expired", "过时", "过期"]):
        score -= 20
    return max(0, min(100, score))


def published_age_days(item: dict, today: date | datetime | str) -> int | None:
    published = parse_published_at(item.get("published_at", ""))
    if not published:
        return None
    report_day = coerce_report_date(today)
    if published.tzinfo:
        published_day = published.astimezone(REPORT_TZ).date()
    else:
        published_day = published.date()
    return (report_day - published_day).days


def classify_recent_seasonal_content_type(item: dict, tags: list[str], text: str, today: date | datetime | str) -> tuple[str, str]:
    age_days = published_age_days(item, today)
    news_signals = ["breaking", "announces", "announced", "launch", "launched", "report", "study", "survey", "policy", "发布", "报告", "研究", "调查", "政策"]
    if age_days is not None and 0 <= age_days <= 7 and has_any(text, news_signals):
        return "今日新闻", "seasonal_recent"
    return "近期文章", "seasonal_recent_analysis"


def load_evergreen_seasonal_items() -> list[dict]:
    if not EVERGREEN_SEASONAL_FILE.exists():
        return []
    with EVERGREEN_SEASONAL_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    return config.get("items", [])


def evergreen_text(item: dict) -> str:
    return " ".join(
        [
            str(item.get("title", "")),
            str(item.get("source", "")),
            " ".join(str(theme) for theme in item.get("themes", [])),
            str(item.get("qiba_angle", "")),
            str(item.get("why_still_relevant", "")),
            str(item.get("notes", "")),
        ]
    )


def evergreen_matches_today(item: dict, today: date | datetime | str) -> bool:
    if not item.get("url"):
        return False
    if item.get("exclude_from_top20") is not True:
        return False
    if item.get("stale_risk") not in {"low", "medium"}:
        return False
    if int(item.get("evergreen_score") or 0) < EVERGREEN_SEASONAL_MIN_SCORE:
        return False
    window = get_seasonal_window(today)
    if window not in item.get("seasonal_windows", []):
        return False
    return True


def build_evergreen_seasonal_item(item: dict, today: date | datetime | str) -> dict:
    themes = item.get("themes", [])
    score = int(item.get("evergreen_score") or 0)
    return {
        "title": item.get("title", ""),
        "source": item.get("source", ""),
        "url": item.get("url", ""),
        "published_at": item.get("published_at", ""),
        "original_year": item.get("original_year", ""),
        "language": item.get("language", ""),
        "region": item.get("region", ""),
        "seasonal_window": get_seasonal_window(today),
        "theme": " / ".join(themes[:3]) if themes else "教育时令",
        "seasonal_topics": themes,
        "seasonal_score": score,
        "priority_score": 0,
        "content_type": item.get("content_type", "经典重读"),
        "topic_type": "seasonal_evergreen_fallback",
        "is_evergreen_fallback": True,
        "exclude_from_top20": True,
        "stale_risk": item.get("stale_risk", ""),
        "seasonal_reason": item.get("why_still_relevant", ""),
        "seasonal_qiba_angle": item.get("qiba_angle", ""),
        "summary": item.get("why_still_relevant", ""),
        "tags": themes,
        "is_seasonal_pick": False,
    }


def build_seasonal_reason(item: dict, tags: list[str], text: str, today: date | datetime | str) -> str:
    theme = classify_seasonal_theme(item, tags, text, today)
    window = get_seasonal_window(today)
    if has_any(theme, ["期末", "考试"]):
        return compact_chinese("当前处在期末和暑假交界，家长最需要的是低焦虑复习、睡眠和成绩沟通，而不是继续加压。", 120)
    if has_any(theme, ["暑假阅读", "暑假书单", "自主阅读", "阅读兴趣", "亲子阅读"]):
        return compact_chinese("暑假前后是阅读计划最容易启动的窗口，这条线索适合讨论书单、自主选书和保护孩子阅读兴趣。", 120)
    if has_any(theme, ["夏季运动", "游泳安全", "户外活动", "儿童运动"]):
        return compact_chinese("暑期运动需求上升，这条线索适合提醒家庭把运动安排、安全边界和长期习惯一起考虑。", 120)
    if has_any(theme, ["亲子游", "旅行学习", "博物馆", "科技馆", "主题乐园", "迪士尼"]):
        return compact_chinese("暑期出行不是纯消费，也可以转成博物馆、科技馆、主题乐园里的观察、学习和亲子关系选题。", 120)
    if has_any(theme, ["夏令营", "营地", "美食营", "食育", "生活技能"]):
        return compact_chinese("暑假前后是营地和生活教育决策期，这条线索适合帮助家长从成长价值、安全和独立性判断。", 120)
    return compact_chinese(f"当前时令窗口是{window}，这条内容与{theme}相关，适合作为近期家庭教育选题储备。", 120)


def build_seasonal_qiba_angle(item: dict, tags: list[str], text: str, today: date | datetime | str) -> str:
    theme = classify_seasonal_theme(item, tags, text, today)
    if has_any(theme, ["期末", "考试"]):
        return compact_chinese("七爸写法可从“期末最该帮孩子稳住节奏，而不是制造二次焦虑”切入。", 120)
    if has_any(theme, ["阅读"]):
        return compact_chinese("七爸写法可从“暑假阅读不是完成书单，而是让孩子重新拥有选书和读下去的动力”切入。", 120)
    if has_any(theme, ["运动", "游泳"]):
        return compact_chinese("七爸写法可从“暑假运动不是报班打卡，而是安全、户外和体能习惯的家庭工程”切入。", 120)
    if has_any(theme, ["亲子游", "旅行", "博物馆", "科技馆", "主题乐园", "迪士尼"]):
        return compact_chinese("七爸写法可从“亲子游最贵的不是门票，而是父母有没有把体验变成孩子的观察和表达”切入。", 120)
    if has_any(theme, ["夏令营", "营地", "食育", "美食营", "生活技能"]):
        return compact_chinese("七爸写法可从“给孩子选暑期项目，先看它训练独立性还是只是在卖焦虑”切入。", 120)
    return compact_chinese("七爸写法可从当前家庭最需要的时令问题切入，落到可执行的亲子沟通和学习安排。", 120)


def build_seasonal_item(item: dict, today: date | datetime | str) -> dict:
    tags = item.get("tags", [])
    text = item_text(item, tags)
    score = score_seasonal_relevance(item, tags, text, today)
    content_type, topic_type = classify_recent_seasonal_content_type(item, tags, text, today)
    return {
        "title": item.get("title", ""),
        "source": item.get("source", ""),
        "url": item.get("link", ""),
        "published_at": item.get("published_at", ""),
        "original_year": "",
        "seasonal_window": get_seasonal_window(today),
        "theme": classify_seasonal_theme(item, tags, text, today),
        "seasonal_topics": matched_seasonal_topics(tags, text, today),
        "seasonal_score": score,
        "priority_score": item.get("priority_score", 0),
        "content_type": content_type,
        "seasonal_reason": build_seasonal_reason(item, tags, text, today),
        "seasonal_qiba_angle": build_seasonal_qiba_angle(item, tags, text, today),
        "topic_type": topic_type,
        "is_evergreen_fallback": False,
        "exclude_from_top20": False,
        "stale_risk": "",
        "summary": item.get("summary", ""),
        "tags": tags,
        "is_seasonal_pick": False,
    }


def select_daily_seasonal_topics(
    items: list[dict],
    today: date | datetime | str,
    evergreen_items: list[dict] | None = None,
    limit: int = SEASONAL_PICK_LIMIT,
) -> list[dict]:
    """Select link-only seasonal topics for the current week.

    The public module is weekly: recent seasonal links are preferred, evergreen
    links only fill gaps, and every selected item must keep a real URL.
    """
    recent_candidates = []
    for item in items:
        if item.get("is_top_pick"):
            continue
        seasonal = build_seasonal_item(item, today)
        if seasonal.get("url") and seasonal["seasonal_score"] >= SEASONAL_MIN_SCORE:
            recent_candidates.append(seasonal)
    recent_candidates.sort(key=lambda item: (item["seasonal_score"], item.get("published_at", "")), reverse=True)

    selected: list[dict] = []
    selected_urls: set[str] = set()
    for seasonal in recent_candidates[:limit]:
        url = seasonal.get("url", "")
        if not url or url in selected_urls:
            continue
        seasonal["is_seasonal_pick"] = True
        selected.append(seasonal)
        selected_urls.add(url)
        if len(selected) == limit:
            return selected

    if len(selected) >= SEASONAL_TARGET_COUNT:
        return selected[:limit]

    evergreen_candidates = []
    for evergreen in evergreen_items or []:
        if not evergreen_matches_today(evergreen, today):
            continue
        seasonal = build_evergreen_seasonal_item(evergreen, today)
        if seasonal.get("url") and seasonal["seasonal_score"] >= EVERGREEN_SEASONAL_MIN_SCORE:
            evergreen_candidates.append(seasonal)
    evergreen_candidates.sort(key=lambda item: (item["seasonal_score"], str(item.get("published_at", ""))), reverse=True)

    needed = min(limit - len(selected), SEASONAL_TARGET_COUNT - len(selected))
    for seasonal in evergreen_candidates:
        if needed <= 0:
            break
        url = seasonal.get("url", "")
        if not url or url in selected_urls:
            continue
        seasonal["is_seasonal_pick"] = True
        selected.append(seasonal)
        selected_urls.add(url)
        needed -= 1
    return selected


def build_digest() -> tuple[Path, Path, Path, Path, Path, Path, Path, Path]:
    rules = load_keyword_rules()
    raw_file = latest_raw_file()
    date_text = raw_file.name.replace(".raw.json", "")
    raw_items = json.loads(raw_file.read_text(encoding="utf-8"))
    evergreen_items = load_evergreen_seasonal_items()
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
        topic_family = classify_topic_family({**item, "tags": tags})
        digest_items.append(
            {
                "title": clean_text(item.get("title", "")),
                "link": link,
                "source": item.get("source", ""),
                "source_category": item.get("source_category", ""),
                "published_at": item.get("published_at", ""),
                "summary": clean_text(item.get("summary", ""))[:300],
                "tags": tags,
                "normalized_title": normalize_title(item.get("title", "")),
                "zh_summary": zh_summary,
                "story_angle": story_angle,
                "qiba_pitch": qiba_pitch,
                "priority_score": priority_score,
                "topic_family": topic_family,
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
    report_date = coerce_report_date(date_text)
    top_items = select_top_picks(digest_items, current_date=report_date)
    selected_by_link = {item["link"]: item for item in top_items}
    top_links = set(selected_by_link)
    for item in digest_items:
        item["is_top_pick"] = item["link"] in top_links
        if item["is_top_pick"]:
            item.update(selected_by_link[item["link"]])
            item["is_top_pick"] = True
    top_items = [dict(item) for item in top_items]
    top_items.sort(key=lambda item: (item["priority_score"], item.get("published_at", "")), reverse=True)
    resource_items = select_daily_resources(digest_items)
    seasonal_items = select_daily_seasonal_topics(digest_items, report_date, evergreen_items)
    week_start = (report_date - timedelta(days=report_date.weekday())).isoformat()
    week_end = (report_date + timedelta(days=6 - report_date.weekday())).isoformat()
    for seasonal_item in seasonal_items:
        seasonal_item["seasonal_period"] = SEASONAL_PERIOD
        seasonal_item["week_start"] = week_start
        seasonal_item["week_end"] = week_end

    json_file = DATA_DIR / f"{date_text}.json"
    md_file = DATA_DIR / f"{date_text}.md"
    top_json_file = DATA_DIR / f"{date_text}_top20.json"
    top_md_file = DATA_DIR / f"{date_text}_top20.md"
    resources_json_file = DATA_DIR / f"{date_text}_resources.json"
    resources_md_file = DATA_DIR / f"{date_text}_resources.md"
    seasonal_json_file = DATA_DIR / f"{date_text}_seasonal.json"
    seasonal_md_file = DATA_DIR / f"{date_text}_seasonal.md"
    archive_index_file = DATA_DIR / "archive_index.json"
    json_file.write_text(json.dumps(digest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    md_file.write_text(render_markdown(date_text, digest_items, "七爸新闻雷达｜完整线索"), encoding="utf-8")
    top_json_file.write_text(json.dumps(top_items, ensure_ascii=False, indent=2), encoding="utf-8")
    top_md_file.write_text(render_markdown(date_text, top_items, "七爸新闻雷达｜今日精选 Top 20"), encoding="utf-8")
    resources_json_file.write_text(json.dumps(resource_items, ensure_ascii=False, indent=2), encoding="utf-8")
    resources_md_file.write_text(render_resources_markdown(date_text, resource_items), encoding="utf-8")
    seasonal_json_file.write_text(json.dumps(seasonal_items, ensure_ascii=False, indent=2), encoding="utf-8")
    seasonal_md_file.write_text(render_seasonal_markdown(date_text, seasonal_items), encoding="utf-8")
    archive_index, archive_data = build_archive_index(DATA_DIR)
    archive_index_file.write_text(json.dumps(archive_index, ensure_ascii=False, indent=2), encoding="utf-8")
    render_html(date_text, top_items, resource_items, seasonal_items, len(digest_items), duplicate_count, archive_index, archive_data)
    print(f"History top20 files found: {len(seen_items['history_files'])}")
    print(f"History top20 files used: {len(seen_items['used_history_files'])}")
    print(f"History top20 items collected: {seen_items['item_count']}")
    print(f"Filtered duplicate candidates: {duplicate_count}")
    if len(seasonal_items) < SEASONAL_TARGET_COUNT:
        print("WARNING: 本周时令选题不足 3 条，原因是 recent 与 evergreen 链接池不足。")
    print(f"Updated archive index: {archive_index_file}")
    return json_file, md_file, top_json_file, top_md_file, resources_json_file, resources_md_file, seasonal_json_file, seasonal_md_file


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


def render_resources_markdown(date_text: str, resources: list[dict]) -> str:
    lines = ["# 七爸新闻雷达｜今日干货资源", "", f"日期：{date_text}", f"数量：{len(resources)}", ""]
    if not resources:
        lines.append("今日暂无高置信干货资源。")
        return "\n".join(lines)
    for index, resource in enumerate(resources, start=1):
        lines.extend(
            [
                f"## {index}. {resource['title']}",
                f"- 来源：{resource['source']}",
                f"- 科目：{resource['subject']}",
                f"- 来源区域：{resource['region']}",
                f"- 年龄段：{resource['age_range']}",
                f"- 资源类型：{resource['resource_type']}",
                f"- 免费/付费：{resource['free_or_paid']}",
                f"- 新鲜度：{resource['freshness']}",
                f"- 资源分数：{resource['score']}",
                f"- 链接：{resource['url']}",
                f"- 推荐理由：{resource['why_useful']}",
                f"- 七爸写法：{resource['qiba_angle']}",
                "",
            ]
        )
    return "\n".join(lines)


def render_seasonal_markdown(date_text: str, seasonal_items: list[dict]) -> str:
    week_start = seasonal_items[0].get("week_start", "") if seasonal_items else ""
    week_end = seasonal_items[0].get("week_end", "") if seasonal_items else ""
    period_line = f"周期：{week_start} 至 {week_end}" if week_start and week_end else "周期：本周"
    lines = ["# 本周时令选题", "", f"生成日期：{date_text}", period_line, f"数量：{len(seasonal_items)}", ""]
    if not seasonal_items:
        lines.append("本周暂无高置信时令链接。建议补充 evergreen_seasonal.yml 或扩展 seasonal sources。")
        return "\n".join(lines)
    for index, item in enumerate(seasonal_items, start=1):
        lines.extend(
            [
                f"## {index}. {item['title']}",
                f"- 来源：{item['source']}",
                f"- 内容类型：{item.get('content_type', '近期文章')}",
                f"- 主题：{item['theme']}",
                f"- 时令窗口：{item['seasonal_window']}",
                f"- 时令分数：{item['seasonal_score']}",
                f"- 话题类型：{item['topic_type']}",
                f"- 原始年份：{item.get('original_year') or '无'}",
                f"- 链接：{item['url']}",
                f"- 推荐理由：{item['seasonal_reason']}",
                f"- 七爸写法：{item['seasonal_qiba_angle']}",
                "",
            ]
        )
    if len(seasonal_items) < SEASONAL_TARGET_COUNT:
        lines.append("本周时令链接不足 3 条，需补充 evergreen_seasonal.yml 或扩展 seasonal sources。")
    return "\n".join(lines)


def script_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_html(
    date_text: str,
    items: list[dict],
    resources: list[dict],
    seasonal_items: list[dict],
    total_count: int,
    duplicate_count: int,
    archive_index: list[dict],
    archive_data: dict[str, list[dict]],
) -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    groups = [
        ("今日必看", "top20_must_read", [item for item in items if item["priority_score"] >= 80]),
        ("可写成文章", "top20_article_candidate", [item for item in items if 65 <= item["priority_score"] <= 79]),
        ("资料储备", "top20_reference", [item for item in items if item["priority_score"] < 65]),
    ]
    resource_section = render_resources_section(resources, date_text)
    seasonal_section = render_seasonal_section(seasonal_items, date_text)
    grouped_sections = "\n".join(render_group(title, section, group_items, date_text) for title, section, group_items in groups)
    shortage_notice = ""
    if len(items) < TOP_PICK_LIMIT:
        shortage_notice = f'<p class="notice">今日去重后不足20条，实际显示 {len(items)} 条。</p>'
    archive_index_json = script_json(archive_index)
    archive_data_json = script_json(archive_data)
    embedded_resources_json = script_json({date_text: resources})
    embedded_seasonal_json = script_json({date_text: seasonal_items})
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
    .rating-tools {{ max-width: 960px; margin: 14px auto 0; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; color: #374151; }}
    .rating-tools strong {{ color: #111827; }}
    .rating-tools button {{ border: 1px solid #d1d5db; border-radius: 8px; background: #ffffff; color: #111827; padding: 7px 10px; cursor: pointer; }}
    .rating-tools button:hover {{ border-color: #f59e0b; color: #92400e; }}
    .notice {{ max-width: 960px; margin: 10px auto 0; color: #9a3412; font-weight: 600; }}
    .group {{ margin-bottom: 28px; }}
    .group-header {{ display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin: 0 0 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; }}
    .group-header h2 {{ margin: 0; font-size: 22px; line-height: 1.3; }}
    .group-count {{ color: #6b7280; font-size: 14px; white-space: nowrap; }}
    .group-note {{ margin: 0 0 14px; color: #4b5563; font-size: 14px; line-height: 1.7; }}
    .empty {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; color: #6b7280; }}
    .item {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 18px; margin-bottom: 16px; }}
    .resource-item {{ border-left: 4px solid #0f766e; }}
    .seasonal-item {{ border-left: 4px solid #b45309; }}
    .meta {{ color: #6b7280; font-size: 14px; margin: 8px 0; }}
    .score-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0; color: #374151; font-size: 14px; }}
    .score-pill {{ background: #ecfdf5; color: #065f46; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .level-pill {{ background: #fff7ed; color: #9a3412; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .resource-pill {{ background: #f0fdfa; color: #115e59; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .seasonal-pill {{ background: #fffbeb; color: #92400e; border-radius: 999px; padding: 4px 10px; font-weight: 600; }}
    .tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0; }}
    .tag {{ background: #eef2ff; color: #3730a3; border-radius: 999px; padding: 3px 9px; font-size: 13px; }}
    .rating-widget {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 10px 0 12px; color: #6b7280; font-size: 14px; }}
    .rating-label {{ font-weight: 600; color: #374151; }}
    .rating-stars {{ display: inline-flex; gap: 2px; }}
    .rating-star {{ border: 0; background: transparent; color: #d1d5db; cursor: pointer; font-size: 22px; line-height: 1; padding: 1px 2px; }}
    .rating-star.is-selected,
    .rating-star.is-preview {{ color: #f59e0b; }}
    .rating-status {{ min-width: 48px; color: #92400e; font-weight: 600; }}
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
    <div class="rating-tools" aria-label="选题评分工具">
      <strong>选题评分</strong>
      <span id="rating-summary">已记录 0 条评分</span>
      <button type="button" id="export-ratings">导出评分 JSON</button>
      <button type="button" id="clear-ratings">清空本地评分</button>
    </div>
    <p class="notice" id="archive-notice">{shortage_notice.replace('<p class="notice">', '').replace('</p>', '')}</p>
  </header>
  <main id="digest-content">
    {resource_section}
    {seasonal_section}
    {grouped_sections}
  </main>
  <script id="archive-index-data" type="application/json">{archive_index_json}</script>
  <script id="archive-items-data" type="application/json">{archive_data_json}</script>
  <script id="archive-resources-data" type="application/json">{embedded_resources_json}</script>
  <script id="archive-seasonal-data" type="application/json">{embedded_seasonal_json}</script>
  <script>
    const embeddedArchiveIndex = JSON.parse(document.getElementById("archive-index-data").textContent);
    const embeddedArchiveData = JSON.parse(document.getElementById("archive-items-data").textContent);
    const embeddedResourcesData = JSON.parse(document.getElementById("archive-resources-data").textContent);
    const embeddedSeasonalData = JSON.parse(document.getElementById("archive-seasonal-data").textContent);
    let archiveIndex = embeddedArchiveIndex;
    const archiveCache = {{ ...embeddedArchiveData }};

    const dateSelect = document.getElementById("archive-date");
    const metaEl = document.getElementById("archive-meta");
    const noticeEl = document.getElementById("archive-notice");
    const contentEl = document.getElementById("digest-content");
    const ratingSummaryEl = document.getElementById("rating-summary");
    const exportRatingsBtn = document.getElementById("export-ratings");
    const clearRatingsBtn = document.getElementById("clear-ratings");
    const ratingStorageKey = "qiba_topic_ratings_v1";
    const ratingAppVersion = "rating-localstorage-v1";

    function escapeHtml(value) {{
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }}

    function withCacheBust(path) {{
      const sep = path.includes("?") ? "&" : "?";
      return `${{path}}${{sep}}v=${{Date.now()}}`;
    }}

    function hashRatingKey(input) {{
      let hash = 5381;
      for (let index = 0; index < input.length; index += 1) {{
        hash = ((hash << 5) + hash) + input.charCodeAt(index);
        hash |= 0;
      }}
      return `qiba_${{Math.abs(hash).toString(36)}}`;
    }}

    function getRatingStore() {{
      try {{
        const raw = localStorage.getItem(ratingStorageKey);
        if (!raw) throw new Error("empty rating store");
        const store = JSON.parse(raw);
        if (!store || typeof store !== "object" || !store.items) throw new Error("invalid rating store");
        return store;
      }} catch (error) {{
        return {{
          app: "qiba-news-radar",
          version: ratingAppVersion,
          updated_at: "",
          items: {{}},
        }};
      }}
    }}

    function saveRatingStore(store) {{
      store.updated_at = new Date().toISOString();
      localStorage.setItem(ratingStorageKey, JSON.stringify(store));
    }}

    function makeItemId(item, section, pageDate) {{
      const url = item.url || item.link || "";
      const identity = url ? `${{section}}|${{pageDate}}|${{url}}` : `${{section}}|${{pageDate}}|${{item.title || ""}}|${{item.source || ""}}`;
      return hashRatingKey(identity);
    }}

    function normalizeRatingPayload(item, section, pageDate, rating) {{
      const itemId = makeItemId(item, section, pageDate);
      return {{
        rating_id: `${{itemId}}:${{Date.now()}}`,
        rated_at: new Date().toISOString(),
        page_date: pageDate,
        section,
        item_id: itemId,
        title: item.title || "",
        source: item.source || "",
        url: item.url || item.link || "",
        rating,
        tags: Array.isArray(item.tags) ? item.tags : [],
        priority_score: item.priority_score ?? null,
        resource_score: item.resource_score ?? item.score ?? null,
        seasonal_score: item.seasonal_score ?? null,
        content_type: item.content_type || item.resource_type || "",
        topic_type: item.topic_type || "",
        seasonal_window: item.seasonal_window || "",
        summary: item.summary || item.why_useful || item.seasonal_reason || "",
        qiba_pitch: item.qiba_pitch || item.qiba_angle || item.seasonal_qiba_angle || "",
        user_note: "",
        app_version: ratingAppVersion,
      }};
    }}

    function getStoredRating(itemId) {{
      const store = getRatingStore();
      return store.items[itemId]?.rating || 0;
    }}

    function setStoredRating(payload) {{
      const store = getRatingStore();
      store.items[payload.item_id] = payload;
      saveRatingStore(store);
    }}

    function removeStoredRating(itemId) {{
      const store = getRatingStore();
      delete store.items[itemId];
      saveRatingStore(store);
    }}

    function renderRatingWidget(item, section, pageDate) {{
      const itemId = makeItemId(item, section, pageDate);
      const payload = normalizeRatingPayload(item, section, pageDate, 0);
      const payloadJson = escapeHtml(JSON.stringify(payload));
      const stars = [1, 2, 3, 4, 5].map((value) => `<button type="button" class="rating-star" data-rating-value="${{value}}" aria-label="${{value}} 星">★</button>`).join("");
      return `<div class="rating-widget" data-item-id="${{escapeHtml(itemId)}}" data-rating-payload="${{payloadJson}}">
  <span class="rating-label">我的评分</span>
  <span class="rating-stars" role="group" aria-label="选题打星">${{stars}}</span>
  <span class="rating-status">未评分</span>
</div>`;
    }}

    function applyRatingToWidget(widget, rating) {{
      widget.querySelectorAll(".rating-star").forEach((star) => {{
        const value = Number(star.dataset.ratingValue || 0);
        star.classList.remove("is-preview");
        star.classList.toggle("is-selected", value <= rating);
        star.setAttribute("aria-pressed", value <= rating ? "true" : "false");
      }});
      const status = widget.querySelector(".rating-status");
      if (status) status.textContent = rating ? `${{rating}} 星` : "未评分";
    }}

    function previewRatingWidget(widget, rating) {{
      widget.querySelectorAll(".rating-star").forEach((star) => {{
        const value = Number(star.dataset.ratingValue || 0);
        star.classList.toggle("is-preview", value <= rating);
        star.classList.toggle("is-selected", false);
      }});
      const status = widget.querySelector(".rating-status");
      if (status) status.textContent = `${{rating}} 星`;
    }}

    function refreshRatingWidgets() {{
      document.querySelectorAll(".rating-widget").forEach((widget) => {{
        applyRatingToWidget(widget, getStoredRating(widget.dataset.itemId));
      }});
      updateRatingSummary();
    }}

    function updateRatingSummary() {{
      const store = getRatingStore();
      const count = Object.keys(store.items || {{}}).length;
      if (ratingSummaryEl) ratingSummaryEl.textContent = `已记录 ${{count}} 条评分`;
    }}

    function exportRatings() {{
      const store = getRatingStore();
      const ratings = Object.values(store.items || {{}});
      const payload = {{
        exported_at: new Date().toISOString(),
        app: "qiba-news-radar",
        version: ratingAppVersion,
        count: ratings.length,
        ratings,
      }};
      const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: "application/json" }});
      const url = URL.createObjectURL(blob);
      const today = new Date().toISOString().slice(0, 10);
      const link = document.createElement("a");
      link.href = url;
      link.download = `qiba-topic-ratings-${{today}}.json`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }}

    function clearRatings() {{
      if (!window.confirm("确定要清空本地所有评分吗？此操作不可恢复。")) return;
      localStorage.removeItem(ratingStorageKey);
      refreshRatingWidgets();
    }}

    function groupItems(items) {{
      return [
        ["今日必看", "top20_must_read", items.filter((item) => Number(item.priority_score || 0) >= 80)],
        ["可写成文章", "top20_article_candidate", items.filter((item) => Number(item.priority_score || 0) >= 65 && Number(item.priority_score || 0) <= 79)],
        ["资料储备", "top20_reference", items.filter((item) => Number(item.priority_score || 0) < 65)],
      ];
    }}

    function renderResourceCard(resource, pageDate) {{
      return `<article class="item resource-item">
  <h2>${{escapeHtml(resource.title || "")}}</h2>
  <p class="meta">${{escapeHtml(resource.subject || "")}}｜${{escapeHtml(resource.region || "")}}｜${{escapeHtml(resource.age_range || "")}}｜${{escapeHtml(resource.resource_type || "")}}｜${{escapeHtml(resource.freshness || "")}}</p>
  <div class="score-row">
    <span class="resource-pill">资源分数：${{escapeHtml(resource.score ?? "")}}</span>
    <span class="level-pill">${{escapeHtml(resource.free_or_paid || "未知")}}</span>
  </div>
  ${{renderRatingWidget(resource, "daily_resource", pageDate)}}
  <section class="news-section">
    <h3>推荐理由</h3>
    <p>${{escapeHtml(resource.why_useful || "暂无推荐理由")}}</p>
  </section>
  <section class="news-section">
    <h3>七爸写法</h3>
    <p>${{escapeHtml(resource.qiba_angle || "暂无七爸写法")}}</p>
  </section>
  <section class="news-section">
    <h3>链接</h3>
    <p><a href="${{escapeHtml(resource.url || "#")}}" target="_blank" rel="noopener noreferrer">打开资源</a></p>
  </section>
</article>`;
    }}

    function renderResourcesSection(resources, pageDate) {{
      const body = resources.length ? resources.map((resource) => renderResourceCard(resource, pageDate)).join("") : '<p class="empty">今日暂无高置信干货资源。</p>';
      return `<section class="group">
  <div class="group-header">
    <h2>今日干货资源</h2>
    <span class="group-count">${{resources.length}} 条</span>
  </div>
  ${{body}}
</section>`;
    }}

    function renderSeasonalCard(item, pageDate) {{
      const year = item.original_year ? ` · ${{escapeHtml(item.original_year)}}` : "";
      return `<article class="item seasonal-item">
  <h2><a href="${{escapeHtml(item.url || "#")}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(item.title || "")}}</a></h2>
  <p class="meta">${{escapeHtml(item.source || "")}}｜${{escapeHtml(item.content_type || "近期文章")}}${{year}}｜${{escapeHtml(item.theme || "")}}｜${{escapeHtml(item.seasonal_window || "")}}</p>
  <div class="score-row">
    <span class="seasonal-pill">时令分数：${{escapeHtml(item.seasonal_score ?? "")}}</span>
    <span class="level-pill">${{escapeHtml(item.topic_type || "seasonal_current")}}</span>
  </div>
  ${{renderRatingWidget(item, "weekly_seasonal", pageDate)}}
  <section class="news-section">
    <h3>推荐理由</h3>
    <p>${{escapeHtml(item.seasonal_reason || "暂无推荐理由")}}</p>
  </section>
  <section class="news-section">
    <h3>七爸写法</h3>
    <p>${{escapeHtml(item.seasonal_qiba_angle || "暂无七爸写法")}}</p>
  </section>
  <section class="news-section">
    <h3>链接</h3>
    <p><a href="${{escapeHtml(item.url || "#")}}" target="_blank" rel="noopener noreferrer">打开原文</a></p>
  </section>
</article>`;
    }}

    function renderSeasonalSection(seasonalItems, pageDate) {{
      const warning = seasonalItems.length && seasonalItems.length < {SEASONAL_TARGET_COUNT} ? '<p class="notice">本周时令链接不足 3 条，需补充 evergreen_seasonal.yml 或扩展 seasonal sources。</p>' : "";
      const body = seasonalItems.length ? seasonalItems.map((item) => renderSeasonalCard(item, pageDate)).join("") + warning : '<p class="empty">本周暂无高置信时令链接。建议补充 evergreen_seasonal.yml 或扩展 seasonal sources。</p>';
      return `<section class="group">
  <div class="group-header">
    <h2>本周时令选题</h2>
    <span class="group-count">${{seasonalItems.length}} 条</span>
  </div>
  <p class="group-note">围绕当前学期与季节，本周最适合七爸关注的 3 个教育/家庭生活选题。</p>
  ${{body}}
</section>`;
    }}

    function renderCard(item, section, pageDate) {{
      const tags = (item.tags || []).map((tag) => `<span class="tag">${{escapeHtml(tag)}}</span>`).join("");
      return `<article class="item">
  <h2><a href="${{escapeHtml(item.link)}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(item.title)}}</a></h2>
  <p class="meta">${{escapeHtml(item.source)}}｜${{escapeHtml(item.published_at || "发布时间未知")}}</p>
  <div class="score-row">
    <span class="score-pill">优先级分数：${{escapeHtml(item.priority_score ?? "")}}</span>
    <span class="level-pill">推荐级别：${{escapeHtml(item.recommendation_level || "")}}</span>
  </div>
  ${{renderRatingWidget(item, section, pageDate)}}
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

    function renderGroup(title, section, items, pageDate) {{
      const body = items.length ? items.map((item) => renderCard(item, section, pageDate)).join("") : '<p class="empty">暂无</p>';
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

    async function loadArchiveResources(entry) {{
      if (!entry.resourcesFile) return [];
      const cacheKey = `${{entry.date}}:resources`;
      if (archiveCache[cacheKey]) return archiveCache[cacheKey];
      try {{
        const response = await fetch(withCacheBust(entry.resourcesFile), {{ cache: "no-store" }});
        if (!response.ok) throw new Error("resources file not found");
        const resources = await response.json();
        archiveCache[cacheKey] = resources;
        return resources;
      }} catch (error) {{
        if (embeddedResourcesData[entry.date]) return embeddedResourcesData[entry.date];
        return [];
      }}
    }}

    async function loadArchiveSeasonal(entry) {{
      if (!entry.seasonalFile) return [];
      const cacheKey = `${{entry.date}}:seasonal`;
      if (archiveCache[cacheKey]) return archiveCache[cacheKey];
      try {{
        const response = await fetch(withCacheBust(entry.seasonalFile), {{ cache: "no-store" }});
        if (!response.ok) throw new Error("seasonal file not found");
        const seasonalItems = await response.json();
        archiveCache[cacheKey] = seasonalItems;
        return seasonalItems;
      }} catch (error) {{
        if (embeddedSeasonalData[entry.date]) return embeddedSeasonalData[entry.date];
        return [];
      }}
    }}

    function renderArchive(entry, items, resources, seasonalItems) {{
      resources = Array.isArray(resources) ? resources : (embeddedResourcesData[entry.date] || []);
      seasonalItems = Array.isArray(seasonalItems) ? seasonalItems : (embeddedSeasonalData[entry.date] || []);
      updateMeta(entry, items);
      contentEl.innerHTML = renderResourcesSection(resources, entry.date) + renderSeasonalSection(seasonalItems, entry.date) + groupItems(items).map(([title, section, group]) => renderGroup(title, section, group, entry.date)).join("");
      dateSelect.value = entry.date;
      const url = new URL(window.location.href);
      url.searchParams.set("date", entry.date);
      window.history.replaceState(null, "", url);
      refreshRatingWidgets();
    }}

    async function loadArchiveIndex() {{
      try {{
        const response = await fetch(withCacheBust("data/archive_index.json"), {{ cache: "no-store" }});
        if (!response.ok) throw new Error("archive index not found");
        archiveIndex = await response.json();
      }} catch (error) {{
        archiveIndex = embeddedArchiveIndex;
      }}
    }}

    async function loadArchiveItems(entry) {{
      if (archiveCache[entry.date]) return archiveCache[entry.date];
      try {{
        const response = await fetch(withCacheBust(entry.top20File), {{ cache: "no-store" }});
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
        const resources = await loadArchiveResources(entry);
        const seasonalItems = await loadArchiveSeasonal(entry);
        renderArchive(entry, items, resources, seasonalItems);
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

    contentEl.addEventListener("click", (event) => {{
      const star = event.target.closest(".rating-star");
      if (!star) return;
      const widget = star.closest(".rating-widget");
      if (!widget) return;
      try {{
        const itemId = widget.dataset.itemId;
        const clickedRating = Number(star.dataset.ratingValue || 0);
        const currentRating = getStoredRating(itemId);
        const nextRating = clickedRating > currentRating ? clickedRating : clickedRating - 1;
        if (nextRating <= 0) {{
          removeStoredRating(itemId);
          applyRatingToWidget(widget, 0);
        }} else {{
          const payload = JSON.parse(widget.dataset.ratingPayload || "{{}}");
          payload.rating = nextRating;
          payload.rated_at = new Date().toISOString();
          payload.rating_id = `${{itemId}}:${{Date.now()}}`;
          setStoredRating(payload);
          applyRatingToWidget(widget, nextRating);
        }}
        updateRatingSummary();
      }} catch (error) {{
        console.warn("Rating update failed", error);
      }}
    }});

    contentEl.addEventListener("mouseover", (event) => {{
      const star = event.target.closest(".rating-star");
      if (!star) return;
      const widget = star.closest(".rating-widget");
      if (!widget) return;
      previewRatingWidget(widget, Number(star.dataset.ratingValue || 0));
    }});

    contentEl.addEventListener("mouseout", (event) => {{
      const widget = event.target.closest(".rating-widget");
      if (!widget) return;
      if (event.relatedTarget && widget.contains(event.relatedTarget)) return;
      applyRatingToWidget(widget, getStoredRating(widget.dataset.itemId));
    }});

    exportRatingsBtn?.addEventListener("click", exportRatings);
    clearRatingsBtn?.addEventListener("click", clearRatings);
    dateSelect.addEventListener("change", () => showDate(dateSelect.value));
    refreshRatingWidgets();
    initArchiveBrowser();
  </script>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")


def render_group(title: str, section: str, items: list[dict], date_text: str) -> str:
    cards = "\n".join(render_card(item, section, date_text) for item in items)
    body = cards or '<p class="empty">暂无</p>'
    return f"""<section class="group">
  <div class="group-header">
    <h2>{escape(title)}</h2>
    <span class="group-count">{len(items)} 条</span>
  </div>
  {body}
</section>"""


def render_resources_section(resources: list[dict], date_text: str) -> str:
    cards = "\n".join(render_resource_card(resource, date_text) for resource in resources)
    body = cards or '<p class="empty">今日暂无高置信干货资源。</p>'
    return f"""<section class="group">
  <div class="group-header">
    <h2>今日干货资源</h2>
    <span class="group-count">{len(resources)} 条</span>
  </div>
  {body}
</section>"""


def render_seasonal_section(seasonal_items: list[dict], date_text: str) -> str:
    cards = "\n".join(render_seasonal_card(item, date_text) for item in seasonal_items)
    warning = ""
    if seasonal_items and len(seasonal_items) < SEASONAL_TARGET_COUNT:
        warning = '<p class="notice">本周时令链接不足 3 条，需补充 evergreen_seasonal.yml 或扩展 seasonal sources。</p>'
    body = (cards + ("\n" + warning if warning else "")) or '<p class="empty">本周暂无高置信时令链接。建议补充 evergreen_seasonal.yml 或扩展 seasonal sources。</p>'
    return f"""<section class="group">
  <div class="group-header">
    <h2>本周时令选题</h2>
    <span class="group-count">{len(seasonal_items)} 条</span>
  </div>
  <p class="group-note">围绕当前学期与季节，本周最适合七爸关注的 3 个教育/家庭生活选题。</p>
  {body}
</section>"""


def render_static_rating_widget(item: dict, section: str, date_text: str) -> str:
    url = item.get("url") or item.get("link") or ""
    identity = f"{section}|{date_text}|{url}" if url else f"{section}|{date_text}|{item.get('title') or ''}|{item.get('source') or ''}"
    item_id = f"qiba_{to_base36(abs(djb2_hash(identity)))}"
    payload = {
        "rating_id": "",
        "rated_at": "",
        "page_date": date_text,
        "section": section,
        "item_id": item_id,
        "title": item.get("title") or "",
        "source": item.get("source") or "",
        "url": url,
        "rating": 0,
        "tags": item.get("tags") if isinstance(item.get("tags"), list) else [],
        "priority_score": item.get("priority_score"),
        "resource_score": item.get("resource_score", item.get("score")),
        "seasonal_score": item.get("seasonal_score"),
        "content_type": item.get("content_type") or item.get("resource_type") or "",
        "topic_type": item.get("topic_type") or "",
        "seasonal_window": item.get("seasonal_window") or "",
        "summary": item.get("summary") or item.get("why_useful") or item.get("seasonal_reason") or "",
        "qiba_pitch": item.get("qiba_pitch") or item.get("qiba_angle") or item.get("seasonal_qiba_angle") or "",
        "user_note": "",
        "app_version": "rating-localstorage-v1",
    }
    payload_json = escape(script_json(payload))
    stars = "".join(f'<button type="button" class="rating-star" data-rating-value="{value}" aria-label="{value} 星">★</button>' for value in range(1, 6))
    return f"""<div class="rating-widget" data-item-id="{escape(item_id)}" data-rating-payload="{payload_json}">
  <span class="rating-label">我的评分</span>
  <span class="rating-stars" role="group" aria-label="选题打星">{stars}</span>
  <span class="rating-status">未评分</span>
</div>"""


def djb2_hash(value: str) -> int:
    result = 5381
    for char in value:
        result = ((result << 5) + result) + ord(char)
        result = ((result + 2**31) % 2**32) - 2**31
    return result


def to_base36(value: int) -> str:
    if value == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    output = ""
    while value:
        value, remainder = divmod(value, 36)
        output = digits[remainder] + output
    return output


def render_resource_card(resource: dict, date_text: str) -> str:
    return f"""<article class="item resource-item">
  <h2>{escape(resource['title'])}</h2>
  <p class="meta">{escape(resource['subject'])}｜{escape(resource['region'])}｜{escape(resource['age_range'])}｜{escape(resource['resource_type'])}｜{escape(resource['freshness'])}</p>
  <div class="score-row">
    <span class="resource-pill">资源分数：{resource['score']}</span>
    <span class="level-pill">{escape(resource['free_or_paid'])}</span>
  </div>
  {render_static_rating_widget(resource, "daily_resource", date_text)}
  <section class="news-section">
    <h3>推荐理由</h3>
    <p>{escape(resource.get('why_useful') or '暂无推荐理由')}</p>
  </section>
  <section class="news-section">
    <h3>七爸写法</h3>
    <p>{escape(resource.get('qiba_angle') or '暂无七爸写法')}</p>
  </section>
  <section class="news-section">
    <h3>链接</h3>
    <p><a href="{escape(resource['url'])}" target="_blank" rel="noopener noreferrer">打开资源</a></p>
  </section>
</article>"""


def render_seasonal_card(item: dict, date_text: str) -> str:
    year = f" · {escape(str(item.get('original_year')))}" if item.get("original_year") else ""
    return f"""<article class="item seasonal-item">
  <h2><a href="{escape(item['url'])}" target="_blank" rel="noopener noreferrer">{escape(item['title'])}</a></h2>
  <p class="meta">{escape(item['source'])}｜{escape(item.get('content_type') or '近期文章')}{year}｜{escape(item['theme'])}｜{escape(item['seasonal_window'])}</p>
  <div class="score-row">
    <span class="seasonal-pill">时令分数：{item['seasonal_score']}</span>
    <span class="level-pill">{escape(item.get('topic_type') or 'seasonal_current')}</span>
  </div>
  {render_static_rating_widget(item, "weekly_seasonal", date_text)}
  <section class="news-section">
    <h3>推荐理由</h3>
    <p>{escape(item.get('seasonal_reason') or '暂无推荐理由')}</p>
  </section>
  <section class="news-section">
    <h3>七爸写法</h3>
    <p>{escape(item.get('seasonal_qiba_angle') or '暂无七爸写法')}</p>
  </section>
  <section class="news-section">
    <h3>链接</h3>
    <p><a href="{escape(item['url'])}" target="_blank" rel="noopener noreferrer">打开原文</a></p>
  </section>
</article>"""


def render_card(item: dict, section: str, date_text: str) -> str:
    tags = "".join(f'<span class="tag">{escape(tag)}</span>' for tag in item["tags"])
    return f"""<article class="item">
  <h2><a href="{escape(item['link'])}" target="_blank" rel="noopener noreferrer">{escape(item['title'])}</a></h2>
  <p class="meta">{escape(item['source'])}｜{escape(item['published_at'] or '发布时间未知')}</p>
  <div class="score-row">
    <span class="score-pill">优先级分数：{item['priority_score']}</span>
    <span class="level-pill">推荐级别：{escape(item['recommendation_level'])}</span>
  </div>
  {render_static_rating_widget(item, section, date_text)}
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
    json_file, md_file, top_json_file, top_md_file, resources_json_file, resources_md_file, seasonal_json_file, seasonal_md_file = build_digest()
    print(f"Saved digest to {json_file} and {md_file}")
    print(f"Saved top picks to {top_json_file} and {top_md_file}")
    print(f"Saved resources to {resources_json_file} and {resources_md_file}")
    print(f"Saved seasonal topics to {seasonal_json_file} and {seasonal_md_file}")
    print(f"Updated {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    main()

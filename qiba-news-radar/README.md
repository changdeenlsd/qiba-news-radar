# qiba-news-radar

七爸新闻雷达｜AI·科技·教育研究日报

当前版本：v0.1 本地可运行版

## 项目用途

这个项目用于每天筛选 AI、高科技、教育研究、美国高校、科技巨头相关的公开 RSS / Atom 新闻，生成一个静态网页日报，供微信公众号作者“七点半爸爸”早上查看选题线索。

v0.1 只使用公开 RSS / Atom 源和本地规则，不调用 OpenAI API，不发送邮件，不做登录系统，也不抓取需要登录或付费墙的网页。项目只保存新闻标题、链接、来源、发布时间、摘要、标签、中文速读和选题建议，不保存全文。

## 当前功能

- 抓取 `sources.yml` 中配置的公开 RSS / Atom 新闻源
- 使用 `keywords.yml` 给新闻打标签
- 为每条新闻生成 `priority_score`
- 保留完整每日线索文件
- 生成 Top 20 精选新闻
- 为新闻生成中文速读
- 为新闻生成选题判断
- 为 Top 20 新闻生成七爸选题建议
- 将首页 `docs/index.html` 按三组展示：
  - 今日必看
  - 可写成文章
  - 资料储备

## 文件说明

- `sources.yml`：新闻源配置
- `keywords.yml`：关键词和标签规则
- `fetch_news.py`：抓取 RSS / Atom 新闻，生成原始 JSON
- `build_digest.py`：计算标签和分数，生成日报、Top 20 和网页
- `requirements.txt`：Python 依赖
- `docs/index.html`：静态网页首页
- `data/`：每天生成的数据文件
- `.github/workflows/daily.yml`：预留的每日自动运行任务

## 本地运行

先安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

然后运行抓取：

```bash
python3 fetch_news.py
```

再生成日报和网页：

```bash
python3 build_digest.py
```

生成结果包括：

- `data/YYYY-MM-DD.raw.json`：原始抓取结果
- `data/YYYY-MM-DD.json`：完整日报数据
- `data/YYYY-MM-DD.md`：完整日报 Markdown
- `data/YYYY-MM-DD_top20.json`：Top 20 精选数据
- `data/YYYY-MM-DD_top20.md`：Top 20 精选 Markdown
- `docs/index.html`：静态网页首页

## 修改 sources.yml

`sources.yml` 用来维护新闻源。每个来源建议包含：

- `name`：来源名称
- `url`：RSS / Atom 地址
- `category`：来源分类
- `region`：地区
- `notes`：备注

示例：

```yaml
sources:
  - name: OpenAI Blog
    url: https://openai.com/news/rss.xml
    category: ai
    region: US
    notes: Official OpenAI news RSS.
```

如果某个来源没有确认稳定 RSS / Atom 地址，先不要编造 URL，可以将 `url` 留空，并在 `notes` 中写明 TODO。

## 修改 keywords.yml

`keywords.yml` 用来维护标签和关键词规则。每个标签建议包含：

- `label`：页面显示的标签名
- `english_keywords`：英文关键词
- `chinese_keywords`：中文关键词
- `keywords`：合并后的关键词列表，供当前脚本匹配使用

示例：

```yaml
tags:
  ai:
    label: AI
    english_keywords:
      - artificial intelligence
      - generative ai
    chinese_keywords:
      - 人工智能
      - 生成式AI
    keywords:
      - artificial intelligence
      - generative ai
      - 人工智能
      - 生成式AI
```

修改关键词后，重新运行：

```bash
python3 build_digest.py
```

如果同时修改了新闻源，再先运行：

```bash
python3 fetch_news.py
```

## 自动运行

GitHub Actions 已预留每日任务，北京时间每天 9:30 运行，对应 UTC 01:30：

```yaml
cron: "30 1 * * *"
```

也保留了 `workflow_dispatch`，方便在 GitHub Actions 页面手动运行。

## 后续计划

- 配置 GitHub Pages，自动部署 `docs/index.html`
- 优化 GitHub Actions 自动提交和发布流程
- 增加邮件推送，把每日 Top 20 发送给作者
- 持续优化评分规则和中文选题建议
- 后续版本可选接入 AI API，但 v0.1 不调用任何 AI API

# 🛰️ ArXiv GPT Intelligence

\> **一款集成了大模型深层分析能力的交互式 ArXiv 论文科研情报面板。**

这是一个基于大语言模型（LLM）的 ArXiv 论文自动化监控与情报分析系统。它能按照您设定的关键词和领域，每日自动抓取最新论文，利用 AI 生成中文核心解读，并通过交互式网页进行管理。

## ✨ 核心功能

- **智能过滤**：支持按 ArXiv 分类（如 `cs.AI`, `cs.CL`）及自定义关键词进行双重筛选。
- **AI 核心总结**：接入火山引擎（豆包）或 DeepSeek API，将晦涩的英文摘要提炼为 3 点式结构化中文情报。
- **增量抓取**：基于 SQLite 数据库的查重机制，确保每篇论文仅处理一次，绝不重复消耗 Token。
- **交互式配置**：无需修改代码，直接在网页端修改监控领域、关键词及抓取上限，并支持**永久保存配置**。
- **多维展示**：提供搜索、统计、展开式阅读及原文直达功能。

------

## 🛠️ 项目结构

```
├── .env                # API 密钥配置文件 (需手动创建)
├── config.py           # 核心参数配置 (支持网页端动态重写)
├── main.py             # 负责抓取、过滤与 AI 总结流水线
├── app.py              # 前端看板：基于 Streamlit 的交互式 Web 界面
├── arxiv_client.py     # 封装 ArXiv API 请求逻辑
├── ai_service.py       # 处理 LLM 接口通信与 Prompt
├── db_manager.py       # SQLite 数据库初始化与读写
├── exporter.py         # 负责导出 Markdown 每日总结
├── arxiv_history.db    # 持久化数据库 (运行后自动生成)
└── reports/            # 存放生成的 Markdown 报告文件夹
```

------

## 🚀 快速开始

### 1. 克隆与环境配置

确保您的电脑已安装 Python 3.10+。

```bash
# 安装核心依赖
pip install streamlit arxiv requests pandas python-dotenv
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件，内容如下：

```ini
VOLC_API_KEY=你的火山引擎API密钥
VOLC_ENDPOINT_ID=你的推理终端ID
```

### 3. 启动系统

本项目采用“前店后厂”模式，所有操作均可在网页端完成：

Bash

```bash
# 启动 Web 看板
python -m streamlit run app.py
```

------

## 📖 使用指南

1. **初始化/抓取**：打开网页侧边栏，设置您感兴趣的 **领域**（如 `cs.LG`）和 **关键词**（如 `RAG`, `Agent`）。
2. **保存并运行**：点击“保存配置并启动抓取”，系统会开始后台作业：
   - 从 ArXiv 拉取最新论文。
   - 通过数据库对比，跳过已读论文。
   - 对命中关键词的论文调用 AI 进行翻译总结。
   - 自动更新 `config.py` 确保下次启动依然生效。
3. **阅读简报**：在主界面通过卡片式列表阅读 AI 总结，点击按钮直达 PDF 原文。

------

## ⚙️ 技术细节

- **数据库**：使用 SQLite 存储 `paper_id`, `title`, `summary`, `url` 及处理时间。
- **动态重载**：`main.py` 采用 `importlib.reload` 技术，确保网页端修改的参数在不重启程序的情况下立即生效。
- **并发保护**：内置 `time.sleep` 与 API 异常处理机制，确保在大规模抓取时的稳定性。

------

## 📅 开发计划 (Roadmap)

- [x] 网页端永久保存参数功能
- [x] 数据库查重增量更新
- [ ] 接入多模型比对 (DeepSeek vs GPT-4)
- [ ] 增加邮件/飞书机器人每日推送
- [ ] 论文趋势热点图谱展示
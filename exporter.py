import os
from datetime import datetime
from config import REPORT_DIR

def save_to_markdown(results_list, prefix="Daily_Research"):
    """
    将处理好的论文列表保存为格式化的 Markdown 文件
    :param results_list: 包含 title, url, date, summary 的字典列表
    :param prefix: 文件名前缀
    :return: 成功保存的文件路径
    """
    # 1. 确保报告目录存在
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        print(f"📂 已创建报告目录: {REPORT_DIR}")

    # 2. 生成基于日期和前缀的文件名
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}_{date_str}.md"
    file_path = os.path.join(REPORT_DIR, filename)

    # 3. 构造 Markdown 内容
    content = []
    content.append(f"# 📚 arXiv 论文深度简报 | {date_str}")
    content.append(f"\n> **统计**: 今日精选 {len(results_list)} 篇论文\n")
    content.append("---\n")

    for i, item in enumerate(results_list, 1):
        content.append(f"## {i}. {item['title']}")
        content.append(f"- **📅 发布日期**: {item['date']}")
        content.append(f"- **🔗 PDF 链接**: [点击查看]({item['url']})")
        content.append(f"\n### 🤖 AI 核心解读\n")
        content.append(f"{item['summary']}")
        content.append("\n---\n")

    # 4. 写入文件
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        return file_path
    except Exception as e:
        print(f"❌ 导出 Markdown 失败: {e}")
        return None

if __name__ == "__main__":
    # 独立测试
    test_data = [{
        "title": "Test Paper",
        "url": "http://arxiv.org/abs/123",
        "date": "2026-01-09",
        "summary": "这是一个测试总结。"
    }]
    save_to_markdown(test_data, "Test_Report")
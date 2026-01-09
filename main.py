import time
import importlib
import sys
import os

# 导入业务模块
from arxiv_client import fetch_latest_papers
from ai_service import summarize_paper
from db_manager import is_paper_processed, record_paper
from exporter import save_to_markdown

def is_interested(title, summary, keywords):
    """关键词匹配过滤"""
    content = (title + summary).lower()
    for kw in keywords:
        if kw.lower() in content:
            return True
    return False

def main():
    """
    执行自动化流水线。
    该函数会被 app.py 调用。
    """
    print("\n" + "="*50)
    print("🚀 --- arXiv 论文自动化情报系统任务启动 ---")
    
    # --- 【核心修复逻辑】确保配置实时重载 ---
    # 1. 检查 config 是否在 sys.modules 中，不在则先导入
    if 'config' not in sys.modules:
        try:
            import config
        except ImportError:
            # 如果路径有问题，强制将当前目录加入路径
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import config
    else:
        # 2. 如果已经在内存中，强制重新从磁盘加载（以获取 app.py 修改后的新参数）
        import config
        importlib.reload(config)
    
    # 打印当前生效的参数，用于调试
    print(f"📊 当前运行参数: ")
    print(f"   - 监控分类: {config.HOT_CATEGORIES}")
    print(f"   - 关键词: {config.FOCUS_KEYWORDS}")
    print(f"   - 抓取上限: {config.MAX_RESULTS_PER_CATEGORY}")
    print("="*50 + "\n")

    # 1. 获取最新论文 (从最新的 config 中读取)
    raw_papers = fetch_latest_papers()
    
    if not raw_papers:
        print("📭 未能获取到论文数据，请检查网络或 arXiv 状态。")
        return

    new_summarized_papers = []
    processed_count = 0

    print(f"🧐 正在扫描 {len(raw_papers)} 篇论文...")

    for paper in raw_papers:
        paper_id = paper.get_short_id()
        title = paper.title
        
        # 2. 查重
        if is_paper_processed(paper_id):
            continue

        # 3. 过滤 (使用刚刚重载后的关键词)
        if is_interested(title, paper.summary, config.FOCUS_KEYWORDS):
            print(f"🔥 命中关键词! 正在分析: {title}")
            
            # 4. AI 总结
            try:
                summary_cn = summarize_paper(title, paper.summary)
                pdf_url = paper.pdf_url
                
                # 5. 写入数据库
                record_paper(
                    paper_id=paper_id, 
                    title=title, 
                    summary=summary_cn, 
                    url=pdf_url
                )
                
                new_summarized_papers.append({
                    "title": title,
                    "url": pdf_url,
                    "date": paper.published.date(),
                    "summary": summary_cn
                })
                
                processed_count += 1
                time.sleep(1) # 保护 API
            except Exception as e:
                print(f"❌ 处理论文 {title} 时出错: {e}")
        else:
            # 不感兴趣也记录，避免下次重复扫描
            record_paper(paper_id, title, "未命中关键词，跳过总结", paper.pdf_url)

    # 6. 任务收尾
    print("\n" + "="*30)
    print(f"✅ 任务完成统计：")
    print(f"- 成功分析并录入: {processed_count} 篇")
    
    if new_summarized_papers:
        report_path = save_to_markdown(new_summarized_papers)
        print(f"📊 本次新增论文报告已生成: {report_path}")
    else:
        print("☕ 本次未发现符合关键词的新论文。")
    print("="*30)

if __name__ == "__main__":
    main()
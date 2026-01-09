import arxiv
import config  # 引入配置模块

def fetch_latest_papers():
    """
    根据 config.py 中的最新参数抓取论文。
    由于 main.py 会执行 reload(config)，这里的变量始终保持最新。
    """
    # 1. 动态获取配置
    categories = config.HOT_CATEGORIES
    max_results = config.MAX_RESULTS_PER_CATEGORY

    # 2. 构建查询字符串
    # 格式如: cat:cs.CL OR cat:cs.AI
    query_string = " OR ".join([f"cat:{cat}" for cat in categories])
    
    print(f"📡 正在从 arXiv 获取数据...")
    print(f"   🔎 查询语句: {query_string}")
    print(f"   🔢 数量上限: {max_results}")

    # 3. 配置客户端
    # delay_seconds 和 num_retries 建议保持稳定，防止被 arXiv 封锁
    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=3,
        num_retries=3
    )

    try:
        search = arxiv.Search(
            query=query_string,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        # 4. 执行抓取并转换为列表
        results = list(client.results(search))
        print(f"✅ 成功抓取到 {len(results)} 篇论文。")
        return results

    except Exception as e:
        print(f"❌ arXiv 抓取过程中出现错误: {e}")
        return []

if __name__ == "__main__":
    # 测试代码
    papers = fetch_latest_papers()
    for p in papers[:3]:
        print(f"测试输出: {p.title}")
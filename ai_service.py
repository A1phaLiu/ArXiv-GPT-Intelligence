import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def _get_client():
    """私有函数：初始化并返回 API 客户端"""
    api_key = os.getenv("VOLC_API_KEY")
    base_url = os.getenv("VOLC_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    
    if not api_key:
        raise ValueError("❌ 错误：未在 .env 中找到 VOLC_API_KEY")
        
    return OpenAI(api_key=api_key, base_url=base_url)

def summarize_paper(title, abstract):
    """
    业务函数：针对论文进行中文总结
    """
    client = _get_client()
    endpoint_id = os.getenv("VOLC_ENDPOINT_ID")
    
    if not endpoint_id:
        return "❌ 总结失败：未配置 VOLC_ENDPOINT_ID"

    system_prompt = "你是一个人工智能领域的顶级研究员，擅长提取论文的核心贡献并用精炼的中文总结。"
    
    user_prompt = f"""请分析以下论文并给出总结：
    标题：{title}
    摘要：{abstract}
    
    要求：
    1. 【核心痛点】：论文解决了什么问题？
    2. 【创新方法】：提出了什么新思路/架构？
    3. 【研究结论】：实验结果如何？
    请直接输出总结内容，不要有开场白，使用 Markdown 格式。
    """

    try:
        completion = client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3  # 较低的随机性保证学术严谨性
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 总结出错: {str(e)}"

if __name__ == "__main__":
    # 模块独立测试逻辑
    test_title = "Scaling Laws for Neural Language Models"
    test_abs = "This paper describes empirical scaling laws for language model performance..."
    print("🧪 正在测试 AI 总结模块...")
    print(summarize_paper(test_title, test_abs))
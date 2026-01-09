import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from datetime import datetime

# 导入业务模块
from main import main as start_main_task
import config # 导入现有配置

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="AI 学术猎手控制台",
    page_icon="🏹",
    layout="wide"
)

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_DB_PATH = os.path.join(BASE_DIR, "arxiv_history.db")

# --- 2. 核心功能函数 ---

def save_config_permanently(categories, keywords, limit):
    """将网页修改的参数永久回写到 config.py 文件"""
    config_path = os.path.join(BASE_DIR, "config.py")
    content = f"""# config.py - 自动生成的配置文件 (更新于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

# 监控的 arXiv 分类
HOT_CATEGORIES = {categories}

# 总结过滤关键词
FOCUS_KEYWORDS = {keywords}

# 每个分类下最大抓取数
MAX_RESULTS_PER_CATEGORY = {limit}

# 存储配置
DB_NAME = "arxiv_history.db"
REPORT_DIR = "reports"
"""
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)

def load_local_data():
    """读取数据库数据"""
    if not os.path.exists(ABS_DB_PATH):
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(ABS_DB_PATH)
        df = pd.read_sql("SELECT * FROM papers ORDER BY processed_at DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"数据库读取失败: {e}")
        return pd.DataFrame()

# --- 3. 侧边栏：参数配置与交互 ---
with st.sidebar:
    st.title("🛠️ 系统配置")
    st.info("在此修改参数将永久同步至 config.py")

    # 配置项 1：领域选择
    all_categories = ["cs.CL", "cs.AI", "cs.LG", "cs.CV", "cs.IR", "cs.RO", "stat.ML"]
    new_cats = st.multiselect(
        "选择监控领域", 
        options=all_categories, 
        default=config.HOT_CATEGORIES
    )

    # 配置项 2：关键词设置
    current_kw_str = ", ".join(config.FOCUS_KEYWORDS)
    new_kw_input = st.text_area("监控关键词 (英文逗号分隔)", value=current_kw_str)
    new_keywords = [k.strip() for k in new_kw_input.split(",") if k.strip()]

    # 配置项 3：抓取数量
    new_limit = st.slider("抓取数量上限", 5, 100, config.MAX_RESULTS_PER_CATEGORY)

    st.divider()

    # 动作按钮
    if st.button("🚀 保存配置并启动抓取", use_container_width=True, type="primary"):
        # 1. 执行永久保存
        save_config_permanently(new_cats, new_keywords, new_limit)
        
        # 2. 启动 main.py 逻辑
        with st.status("正在同步数据...", expanded=True) as status:
            try:
                # 重新加载模块或直接传入参数运行
                # 这里我们直接运行 main()，它会自动读取刚刚保存的 config.py
                start_main_task()
                status.update(label="✅ 更新完成!", state="complete", expanded=False)
                st.toast("配置已保存，数据已更新！")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"运行失败: {e}")
                status.update(label="❌ 出错", state="error")

    st.divider()
    search_term = st.text_input("🔍 搜索库中论文", "")

# --- 4. 主界面：内容展示 ---
st.title("📚 AI 论文智能看板")

df = load_local_data()

if df.empty:
    st.warning("📭 数据库为空。请在左侧配置好参数后点击“启动抓取”。")
else:
    # 搜索过滤
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False) | 
                df['summary'].str.contains(search_term, case=False)]

    # 统计指标
    c1, c2, c3 = st.columns(3)
    c1.metric("论文总数", len(df))
    c2.metric("当前领域数", len(config.HOT_CATEGORIES))
    c3.metric("最后更新时间", df['processed_at'].iloc[0][:16])

    st.divider()

    # 论文列表渲染
    for idx, row in df.iterrows():
        with st.expander(f"📅 {row['processed_at'][:10]} | {row['title']}", expanded=(idx == 0)):
            col_main, col_side = st.columns([3, 1])
            
            with col_main:
                st.markdown("##### 🤖 AI 深度总结")
                st.markdown(row['summary'])
            
            with col_side:
                st.markdown("##### 📄 信息")
                st.write(f"ID: `{row['paper_id']}`")
                st.link_button("🔗 查看原文", row['url'], use_container_width=True)
            
            st.divider()

# --- 页脚 ---
st.caption("Powered by Gemini & Streamlit | 您的专属学术情报员")
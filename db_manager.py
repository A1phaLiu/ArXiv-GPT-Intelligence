import sqlite3
from datetime import datetime

DB_NAME = "arxiv_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                paper_id TEXT PRIMARY KEY,
                title TEXT,
                summary TEXT,    -- 存储 AI 总结
                url TEXT,        -- 存储 PDF 链接
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def is_paper_processed(paper_id):
    """高效查询 ID 是否存在 (O(log N))"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM papers WHERE paper_id = ?', (paper_id,))
        return cursor.fetchone() is not None

def record_paper(paper_id, title, summary, url):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # 确保插入所有 4 个字段
        cursor.execute(
            'INSERT OR IGNORE INTO papers (paper_id, title, summary, url) VALUES (?, ?, ?, ?)', 
            (paper_id, title, summary, url)
        )
        conn.commit()

# 模块加载时自动初始化
init_db()
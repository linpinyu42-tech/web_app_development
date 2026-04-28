import sqlite3
import os

# 定義資料庫檔案的絕對路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線，並將結果轉換為字典形式 (sqlite3.Row)"""
    # 確保 instance 資料夾存在
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Book:
    @staticmethod
    def init_db():
        """初始化資料庫，建立資料表"""
        schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            conn = get_db_connection()
            conn.executescript(schema_script)
            conn.commit()
            conn.close()

    @staticmethod
    def create(title, read_date=None, notes=None, rating=None, category=None):
        """新增一筆書籍筆記"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, read_date, notes, rating, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, read_date, notes, rating, category))
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return book_id

    @staticmethod
    def get_all():
        """取得所有書籍筆記，依照建立時間倒序排列"""
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
        conn.close()
        return books

    @staticmethod
    def get_by_id(book_id):
        """根據 ID 取得單筆書籍筆記"""
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        return book

    @staticmethod
    def update(book_id, title, read_date=None, notes=None, rating=None, category=None):
        """更新特定 ID 的書籍筆記"""
        conn = get_db_connection()
        conn.execute('''
            UPDATE books
            SET title = ?, read_date = ?, notes = ?, rating = ?, category = ?
            WHERE id = ?
        ''', (title, read_date, notes, rating, category, book_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id):
        """刪除特定 ID 的書籍筆記"""
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()

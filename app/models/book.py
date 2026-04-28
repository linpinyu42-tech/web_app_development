import sqlite3
import os
import logging

# 設定 logging，方便除錯
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定義資料庫檔案的絕對路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """
    取得 SQLite 資料庫連線，並將結果轉換為字典形式 (sqlite3.Row)
    """
    try:
        # 確保 instance 資料夾存在
        os.makedirs(DB_DIR, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"資料庫連線失敗: {e}")
        raise

class Book:
    @staticmethod
    def init_db():
        """初始化資料庫，建立資料表"""
        try:
            schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_script = f.read()
                conn = get_db_connection()
                conn.executescript(schema_script)
                conn.commit()
                conn.close()
                logger.info("資料庫與資料表初始化成功。")
            else:
                logger.warning(f"找不到 schema 檔案: {schema_path}")
        except sqlite3.Error as e:
            logger.error(f"初始化資料庫失敗: {e}")
            raise
        except Exception as e:
            logger.error(f"讀取 schema 檔案發生錯誤: {e}")
            raise

    @staticmethod
    def create(title, read_date=None, notes=None, rating=None, category=None):
        """
        新增一筆書籍筆記
        :param title: 書名 (必填)
        :param read_date: 閱讀日期
        :param notes: 讀後心得
        :param rating: 評分 (1~5)
        :param category: 書籍分類
        :return: 新增的書籍 ID，若失敗則回傳 None
        """
        try:
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
        except sqlite3.Error as e:
            logger.error(f"新增書籍記錄失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有書籍筆記，依照建立時間倒序排列
        :return: 書籍記錄列表 (sqlite3.Row)，若失敗則回傳空列表 []
        """
        try:
            conn = get_db_connection()
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            conn.close()
            return books
        except sqlite3.Error as e:
            logger.error(f"取得所有書籍記錄失敗: {e}")
            return []

    @staticmethod
    def get_by_id(book_id):
        """
        根據 ID 取得單筆書籍筆記
        :param book_id: 書籍 ID
        :return: 單筆記錄 (sqlite3.Row)，若找不到或失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            conn.close()
            return book
        except sqlite3.Error as e:
            logger.error(f"取得單筆書籍記錄失敗 (ID: {book_id}): {e}")
            return None

    @staticmethod
    def update(book_id, title, read_date=None, notes=None, rating=None, category=None):
        """
        更新特定 ID 的書籍筆記
        :param book_id: 書籍 ID
        :param title: 書名 (必填)
        :param read_date: 閱讀日期
        :param notes: 讀後心得
        :param rating: 評分 (1~5)
        :param category: 書籍分類
        :return: Boolean 表示是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE books
                SET title = ?, read_date = ?, notes = ?, rating = ?, category = ?
                WHERE id = ?
            ''', (title, read_date, notes, rating, category, book_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"更新書籍記錄失敗 (ID: {book_id}): {e}")
            return False

    @staticmethod
    def delete(book_id):
        """
        刪除特定 ID 的書籍筆記
        :param book_id: 書籍 ID
        :return: Boolean 表示是否成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"刪除書籍記錄失敗 (ID: {book_id}): {e}")
            return False

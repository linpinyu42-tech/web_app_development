from app import create_app
from app.models.book import Book

app = create_app()

def init_db():
    """初始化資料庫與資料表"""
    Book.init_db()
    print("資料庫初始化完成！")

if __name__ == '__main__':
    # 啟動應用程式前，確保資料庫與資料表已經建立
    init_db()
    # 啟動 Flask 開發伺服器
    app.run(debug=True)

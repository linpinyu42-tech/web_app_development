from flask import Flask
from app.routes.book_routes import book_bp

def create_app():
    app = Flask(__name__)
    
    # 設定 SECRET_KEY 用於 session 與 flash message
    # 在實際的專案中，應該從環境變數讀取
    app.config['SECRET_KEY'] = 'dev_secret_key_for_flash_messages'
    
    # 註冊 Blueprint，將 routes 集中管理
    app.register_blueprint(book_bp)
    
    return app

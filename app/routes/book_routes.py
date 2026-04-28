from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.book import Book  # 實作時再解除註解

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/')
def index():
    """
    首頁：顯示所有讀書筆記
    邏輯：呼叫 Book.get_all() 取得資料，傳入 index.html 渲染。
    """
    pass

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    新增筆記頁面：顯示空白表單
    邏輯：渲染 add.html
    """
    pass

@book_bp.route('/books', methods=['POST'])
def create_book():
    """
    建立筆記：接收表單資料寫入 DB
    邏輯：
    1. 取得 request.form 資料
    2. 驗證必填欄位 (title)
    3. 呼叫 Book.create(...)
    4. 成功後重導向至首頁
    """
    pass

@book_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    筆記詳情：顯示單筆筆記
    邏輯：
    1. 呼叫 Book.get_by_id(id)
    2. 若找不到回傳 404
    3. 渲染 detail.html
    """
    pass

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    編輯筆記頁面：顯示帶有原資料的表單
    邏輯：
    1. 呼叫 Book.get_by_id(id)
    2. 若找不到回傳 404
    3. 渲染 edit.html
    """
    pass

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    更新筆記：接收表單資料並更新 DB
    邏輯：
    1. 取得 request.form 資料並驗證
    2. 呼叫 Book.update(...)
    3. 成功後重導向至詳情頁
    """
    pass

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除筆記：從 DB 刪除單筆資料
    邏輯：
    1. 呼叫 Book.delete(id)
    2. 重導向至首頁
    """
    pass

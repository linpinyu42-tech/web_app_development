from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.book import Book

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/')
def index():
    """
    首頁：顯示所有讀書筆記
    邏輯：呼叫 Book.get_all() 取得資料，傳入 index.html 渲染。
    """
    books = Book.get_all()
    return render_template('index.html', books=books)

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    新增筆記頁面：顯示空白表單
    邏輯：渲染 add.html
    """
    return render_template('add.html')

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
    title = request.form.get('title')
    read_date = request.form.get('read_date')
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    category = request.form.get('category')

    if not title:
        flash('書名為必填欄位！', 'danger')
        return render_template('add.html', 
                               read_date=read_date, 
                               notes=notes, 
                               rating=rating, 
                               category=category)

    if rating:
        try:
            rating = int(rating)
        except ValueError:
            rating = None

    book_id = Book.create(title=title, read_date=read_date, notes=notes, rating=rating, category=category)
    
    if book_id:
        flash('筆記新增成功！', 'success')
        return redirect(url_for('book_bp.index'))
    else:
        flash('新增筆記時發生錯誤，請稍後再試。', 'danger')
        return render_template('add.html', 
                               title=title,
                               read_date=read_date, 
                               notes=notes, 
                               rating=rating, 
                               category=category)

@book_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    筆記詳情：顯示單筆筆記
    邏輯：
    1. 呼叫 Book.get_by_id(id)
    2. 若找不到回傳 404
    3. 渲染 detail.html
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('detail.html', book=book)

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    編輯筆記頁面：顯示帶有原資料的表單
    邏輯：
    1. 呼叫 Book.get_by_id(id)
    2. 若找不到回傳 404
    3. 渲染 edit.html
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('edit.html', book=book)

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    更新筆記：接收表單資料並更新 DB
    邏輯：
    1. 取得 request.form 資料並驗證
    2. 呼叫 Book.update(...)
    3. 成功後重導向至詳情頁
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)

    title = request.form.get('title')
    read_date = request.form.get('read_date')
    notes = request.form.get('notes')
    rating = request.form.get('rating')
    category = request.form.get('category')

    if not title:
        flash('書名為必填欄位！', 'danger')
        temp_book = {
            'id': id,
            'title': title,
            'read_date': read_date,
            'notes': notes,
            'rating': rating,
            'category': category
        }
        return render_template('edit.html', book=temp_book)

    if rating:
        try:
            rating = int(rating)
        except ValueError:
            rating = None

    success = Book.update(book_id=id, title=title, read_date=read_date, notes=notes, rating=rating, category=category)
    
    if success:
        flash('筆記更新成功！', 'success')
        return redirect(url_for('book_bp.book_detail', id=id))
    else:
        flash('更新筆記時發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('book_bp.edit_book', id=id))

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除筆記：從 DB 刪除單筆資料
    邏輯：
    1. 呼叫 Book.delete(id)
    2. 重導向至首頁
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)

    success = Book.delete(id)
    if success:
        flash('筆記已成功刪除！', 'success')
    else:
        flash('刪除筆記時發生錯誤。', 'danger')
        
    return redirect(url_for('book_bp.index'))

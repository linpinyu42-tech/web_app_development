# 讀書筆記本系統 - 路由設計文件 (ROUTES)

本文件根據功能需求與資料庫設計，規劃了 Flask 應用程式的路由架構與 Jinja2 模板的對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (筆記列表) | GET | `/` | `index.html` | 顯示所有讀書筆記，依照建立時間排序 |
| 新增筆記頁面 | GET | `/books/new` | `add.html` | 顯示新增筆記的空白表單 |
| 建立筆記 | POST | `/books` | — (重導向至 `/`) | 接收表單資料，寫入資料庫後重導向回首頁 |
| 筆記詳情 | GET | `/books/<int:id>` | `detail.html` | 顯示特定書籍的詳細心得與評分 |
| 編輯筆記頁面 | GET | `/books/<int:id>/edit` | `edit.html` | 顯示載入既有資料的表單，供使用者修改 |
| 更新筆記 | POST | `/books/<int:id>/update` | — (重導向至詳情或首頁) | 接收修改後的資料，更新資料庫 |
| 刪除筆記 | POST | `/books/<int:id>/delete` | — (重導向至 `/`) | 刪除特定書籍紀錄後重導向回首頁 |

*(註：因 HTML 表單原生不支援 PUT 與 DELETE 方法，故遵循 RESTful 妥協慣例，更新與刪除操作改以 POST 處理。)*

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **處理邏輯**：呼叫 `Book.get_all()` 取得所有書籍資料。
- **輸出**：渲染 `index.html`，並將書籍資料列表傳入模板。
- **錯誤處理**：若資料庫內無資料，模板應顯示「目前尚無筆記」的提示訊息。

### `GET /books/new` (新增筆記頁面)
- **處理邏輯**：無需特殊資料處理，直接渲染畫面。
- **輸出**：渲染 `add.html`。

### `POST /books` (建立筆記)
- **輸入**：表單欄位 `title` (必填), `read_date`, `notes`, `rating`, `category`。
- **處理邏輯**：
  1. 驗證 `title` 是否有值。
  2. 呼叫 `Book.create(...)` 將資料存入 SQLite。
- **輸出**：處理完成後，使用 `redirect` 導向回 `GET /`。
- **錯誤處理**：若 `title` 為空，可使用 `flash()` 顯示錯誤訊息，並重新渲染 `add.html`，保留使用者已填寫的內容。

### `GET /books/<int:id>` (筆記詳情)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)`。
- **輸出**：渲染 `detail.html`，並傳入單筆書籍資料。
- **錯誤處理**：若資料庫內找不到該 `id`，回傳 404 頁面，或顯示「找不到該筆資料」的錯誤訊息後導回首頁。

### `GET /books/<int:id>/edit` (編輯筆記頁面)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)` 取出舊有資料。
- **輸出**：渲染 `edit.html`，並將取得的舊資料填入表單預設值。
- **錯誤處理**：若找不到該 `id`，回傳 404 頁面。

### `POST /books/<int:id>/update` (更新筆記)
- **輸入**：URL 路徑參數 `id` 與修改後的表單欄位資料。
- **處理邏輯**：
  1. 驗證 `title` 是否有值。
  2. 呼叫 `Book.update(...)` 更新資料庫內相對應的欄位。
- **輸出**：更新成功後重導向至 `GET /books/<id>` (詳情頁)。
- **錯誤處理**：若驗證失敗，重新渲染 `edit.html` 顯示錯誤。

### `POST /books/<int:id>/delete` (刪除筆記)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `Book.delete(id)` 刪除該筆紀錄。
- **輸出**：刪除成功後重導向至 `GET /` (首頁)。

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html`，以保持網站風格與導覽列的一致性。

- `base.html`：基底模板，包含 HTML 骨架、共用的 CSS 連結、Header 與 Navbar。
- `index.html`：首頁模板，顯示系統簡介與所有書籍的列表。
- `add.html`：新增表單模板。
- `edit.html`：編輯表單模板（結構與 add 相似，但有預設值與不同的 `action` 網址）。
- `detail.html`：單筆書籍詳細資訊與完整心得的展示頁面。

## 4. 路由骨架程式碼

已於 `app/routes/book_routes.py` 建立 Flask Blueprint 與路由函式骨架（僅定義函式與 docstring，尚未實作邏輯）。

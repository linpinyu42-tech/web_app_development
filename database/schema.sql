CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    read_date TEXT,
    notes TEXT,
    rating INTEGER,
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE_TABLE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category INTEGER,
    size TEXT,
    price REAL,
    article INTEGER,
    photo
    )
"""

INSERT_PRODUCTS = """
    INSERT INTO products (name, category, size, price, article, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""
CREATE_TABLE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category INTEGER,
    size TEXT,
    price REAL,
    article INTEGER UNIQUE,
    photo
    )
"""

INSERT_PRODUCTS = """
    INSERT INTO products (name, category, size, price, article, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""

CREATE_TABLE_ORDERS = """
    CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_article INTEGER,
    size TEXT,
    count INTEGER,
    phone_number TEXT,
    FOREIGN KEY (product_article) REFERENCES products(article) ON DELETE CASCADE
    )
"""

INSERT_ORDERS = """
    INSERT INTO orders (product_article, size, count, phone_number)
    VALUES (?, ?, ?, ?)
"""
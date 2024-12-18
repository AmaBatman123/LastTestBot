import sqlite3
from db import queries
import aiosqlite

db = sqlite3.connect('db/products')
cursor = db.cursor()

async def sql_create():
    if db:
        print('Database connected')
    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_ORDERS)
    db.commit()

    # Запись FSM_Products
#=================================================================

async def sql_insert_products(name, category, size, price, article, photo):
    cursor.execute(queries.INSERT_PRODUCTS, (
        name, category, size, price, article, photo
    ))
    db.commit()

async def sql_insert_orders(product_article, size, count, phone_number):
    cursor.execute(queries.INSERT_ORDERS, (
        product_article, size, count, phone_number
    ))
    db.commit()

    # CRUD - Read
#=================================================================

async def get_db_connection():
    conn = sqlite3.connect('db/products')
    conn.row_factory = aiosqlite.Row
    return conn

async def fetch_all_products():
    conn = await get_db_connection()
    products =  conn.execute("""
        SELECT * FROM products
    """).fetchall()
    conn.close()
    return products

async def is_product_article(article):
    conn = await get_db_connection()
    product = conn.execute("""
        SELECT * FROM products WHERE article = ?
    """, (article,)).fetchone()
    conn.close()
    return product




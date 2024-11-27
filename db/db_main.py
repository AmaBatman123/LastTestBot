import sqlite3
from itertools import product

from db import queries
import aiosqlite

db = sqlite3.connect('db/products')
cursor = db.cursor()

async def sql_create():
    if db:
        print('Database connected')
    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    db.commit()

    # Запись FSM_Products
#=================================================================

async def sql_insert_products(name, category, size, price, article, photo):
    cursor.execute(queries.INSERT_PRODUCTS, (
        name, category, size, price, article, photo
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
    products = conn.execute("""
        SELECT * FROM products
    """).fetchall()
    conn.close()
    return products


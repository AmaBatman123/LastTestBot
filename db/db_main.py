import sqlite3
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
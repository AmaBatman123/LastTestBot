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

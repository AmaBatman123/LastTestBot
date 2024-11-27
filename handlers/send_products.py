from itertools import product

from aiogram import  types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import db_main

async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all')
    keyboard.add(btn_all)

    await message.answer('Вы хотите посмотреть все товары?', reply_markup=keyboard)

async def send_products(callback_query: types.CallbackQuery):
    products = await db_main.fetch_all_products()
    if products:
        for product in products:
            caption = (
                f'Название - {product["name"]}\n'
                f'Категория - {product["category"]}\n'
                f'Размер - {product["size"]}\n'
                f'Цена - {product["price"]}\n'
                f'Артикул - {product["article"]}\n'
            )

        await callback_query.message.answer_photo(
            photo=product["photo"],
            caption=caption
        )
    else:
        await callback_query.message.answer(text='В базе сейчас нет товаров')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products'])
    dp.register_callback_query_handler(send_products, Text(equals='all'))
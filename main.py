from config import bot, dp, is_staff
from aiogram import executor
from db import db_main
from handlers import commands, fsm_products, send_products, fsm_order
import logging

commands.register_commands_handler(dp)
fsm_order.register_fsm_order_handler(dp)
send_products.register_handlers(dp)
if is_staff:
    fsm_products.register_fsm_products_handler(dp)

chat_id = '372040467'

async def on_startup(dp):
    await bot.send_message(chat_id=chat_id, text='Bot started!')
    await db_main.sql_create()

async def on_shutdown(dp):
    await bot.send_message(chat_id=chat_id, text='Bot stopped!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)


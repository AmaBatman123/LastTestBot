from aiogram import types, Dispatcher
from config import bot

async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет {message.from_user.first_name} \n'
                                f'Рад приветствовать тебя в нашем интернет магазине! \n'
                                f'Твой ID - {message.from_user.id} \n'
                                f'Будешь много покупать, деньги закончатся')

async def about_bot(message: types.Message):
    try:
        info_text = ("Данный бот предназначен для работы с интернет"
                     "магазином и используется исключительно в учебных целях"
                     "Доступные команды: \n /start \n /info \n /products \n /order \n /add_product(для персонала)")
        await message.answer(info_text)
    except Exception as e:
        await message.answer(text=f'Произошла ошибка {e}')

def register_commands_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(about_bot, commands=['info'])
from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

staff = [
    {'id': 372040467, 'name': 'Valerii'}
        ]

token = config('TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def is_staff(user_id: int) -> bool:
    return any(staff_member['id'] == user_id for staff_member in staff)
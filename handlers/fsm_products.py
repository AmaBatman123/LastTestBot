from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from buttons import cancel, confirm_kb, sizes_kb
from db import db_main
from config import is_staff

class fsm_product(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()
    article =State()
    photo = State()

async def start_fsm(message: types.Message):
    if not await is_staff(message.from_user.id):
        await message.answer('У вас нет доступа к этой команде!')
        return
    else:
        await message.answer('Введите название товара: ', reply_markup=cancel)
        await fsm_product.name.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await fsm_product.next()
    await message.answer('Выберите категорию товара: ', reply_markup=cancel)

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await fsm_product.next()
    await message.answer('Определите размер товара: ', reply_markup=sizes_kb)

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await fsm_product.next()
    await message.answer('Определите цену на товар: ', reply_markup=cancel)

async def load_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Цена должна быть числом!')
        return

    async with state.proxy() as data:
        data['price'] = int(message.text)

    await fsm_product.next()
    await message.answer('Дайте артикул товару: ', reply_markup=cancel)

async def load_article_product(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Артикул должен быть числом!')
        return

    async with state.proxy() as data:
        data['article'] = message.text

    await fsm_product.next()
    await message.answer('Загрузите фото товара ', reply_markup=cancel)

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await message.answer_photo(photo=data['photo'],
                                   caption=f'Название - {data["name"]} \n'
                                            f'Категория - {data["category"]} \n'
                                            f'Размер - {data["size"]} \n'
                                            f'Цена - {data["price"]} \n'
                                            f'Артикул - {data["article"]} \n')

        await message.answer('Верны ли данные?', reply_markup=confirm_kb)

async def confirm_fsm(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Товар занесен в базу', reply_markup=ReplyKeyboardRemove())
        async with state.proxy() as data:
            await db_main.sql_insert_products(
                name = data['name'],
                category = data['category'],
                size = data['size'],
                price = data['price'],
                article = data['article'],
                photo = data['photo']
            )
            await state.finish()
    elif message.text == 'Нет':
        await state.finish()
        await message.answer('Отменено...', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Выберите Да/Нет')
        await state.finish()

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)

def register_fsm_products_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state=fsm_product)
    dp.register_message_handler(confirm_fsm, Text(equals=['Да','Нет']),state=fsm_product)
    dp.register_message_handler(start_fsm, commands=['add_product'])
    dp.register_message_handler(load_name, state=fsm_product.name)
    dp.register_message_handler(load_category, state=fsm_product.category)
    dp.register_message_handler(load_size, state=fsm_product.size)
    dp.register_message_handler(load_price, state=fsm_product.price)
    dp.register_message_handler(load_article_product, state=fsm_product.article)
    dp.register_message_handler(load_photo, state=fsm_product.photo, content_types=['photo'])
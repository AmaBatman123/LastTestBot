from itertools import product

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from buttons import cancel, confirm_order, sizes_order
from db import db_main


class fsm_order(StatesGroup):
    article = State()
    size = State()
    count = State()
    phone_number = State()

async def on_start_order(message: types.Message):
    await message.answer('Введите артикул товара для заказа: ', reply_markup=cancel)
    await fsm_order.article.set()

async def load_article_order(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Артикул должен быть числом!')
        return

    order_article = int(message.text)

    order_product = await db_main.is_product_article(order_article)
    if not order_product:
        await message.answer('В базе нет такого товара, либо его распродали!')
        return

    async with state.proxy() as data:
        data['product_article'] = int(message.text)

    await fsm_order.next()
    await message.answer('Выберите размер', reply_markup=sizes_order)

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await fsm_order.next()
    await message.answer('Укажите количество', reply_markup=cancel)

async def load_count(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Количество должно быть целым числом!')
        return

    async with state.proxy() as data:
        data['count'] = int(message.text)

    await fsm_order.next()
    await message.answer('Введите номер, для обратной связи: ', reply_markup=cancel)

async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    order_summary = (
        f"Ваш заказ:\n"
        f"Артикул: {data['product_article']}\n"
        f"Размер: {data['size']}\n"
        f"Количество: {data['count']}\n"
        f"Номер для связи: {data['phone_number']}\n"
    )
    await message.answer(order_summary, reply_markup=confirm_order)

async def confirm_order_func(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Да':
            await message.answer('Заказ передан, спасибо!', reply_markup=ReplyKeyboardRemove())
            async with state.proxy() as data:
                await db_main.sql_insert_orders(
                    product_article=data['product_article'],
                    size=data['size'],
                    count=data['count'],
                    phone_number=data['phone_number']
                )
                await state.finish()
        elif message.text == 'Нет':
            await state.finish()
            await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Введите Да или Нет')
            await state.finish()
    except Exception as e:
        await message.answer(f'Ошибка {e}')
        await state.finish()

async def cancel_order(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)

def register_fsm_order_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_order, Text(equals='Отмена', ignore_case=True), state=fsm_order)
    dp.register_message_handler(confirm_order_func, Text(equals=['Да', 'Нет']), state=fsm_order.phone_number)
    dp.register_message_handler(on_start_order, commands=['order'])
    dp.register_message_handler(load_article_order, state=fsm_order.article)
    dp.register_message_handler(load_size, state=fsm_order.size)
    dp.register_message_handler(load_count, state=fsm_order.count)
    dp.register_message_handler(load_phone_number, state=fsm_order.phone_number)


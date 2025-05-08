import asyncio

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Database
from keyboards import cancel_keyboard, return_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, F, types



bot = Bot('YOUR BOT TOKEN')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

db = Database('database.db')
BOT_NICKNAME = 'YOUR BOT NICKNAME'




class Send(StatesGroup):
    send = State()
    send_answer = State()


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    db.create_tables()

    question_photo_path = 'fotos/anonimous_q.jpg'
    # errno_photo_path = 'fotos/erno.jpg'

    ID = message.from_user.id
    start_command = message.text
    refferer = start_command[7:]
    ref_link = f'https://t.me/{BOT_NICKNAME}?start={ID}h'

    markup = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="💌 Отправить ссылку",
                                  switch_inline_query=f"🥺 Отправь мне сообщение:\n\n {ref_link}")
    markup.add(button)


    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.username)
        db.set_signup(message.from_user.id, 'done')
        await message.answer_photo(photo=FSInputFile(question_photo_path),
                                   caption=f'<b>Привет, {message.from_user.first_name}, это бот анонимных вопросов!</b>\n\n'
                                           f'<b>Твоя ссылкa для вопросов:</b>\n'
                                           f'{ref_link}\n\n'
                                           f'Покажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!',
                                   parse_mode='html', reply_markup=markup.as_markup())

    else:
        if 'h' in str(refferer):
            refferer_new = str(refferer).replace('h', '')
            refferer2 = int(refferer_new)

            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)
                db.set_nickname(message.from_user.id, message.from_user.username)
                db.set_signup(message.from_user.id, 'done')

            db.set_sender(message.from_user.id, message.from_user.id)
            db.set_sender2(message.from_user.id, refferer2)
            await message.answer('Введите ваш вопрос:', parse_mode='html', reply_markup=cancel_keyboard())
            await state.set_state(Send.send)

        else:
            await message.answer_photo(photo=FSInputFile(question_photo_path),
                                   caption=f'<b>Привет, {message.from_user.first_name}, это бот анонимных вопросов!</b>\n\n'
                                           f'<b>Твоя ссылкa для вопросов:</b>\n'
                                           f'{ref_link}\n\n'
                                           f'Покажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!',
                                   parse_mode='html', reply_markup=markup.as_markup())


@dp.callback_query(StateFilter(Send.send, Send.send_answer))
async def cancel_action(callback_query: CallbackQuery, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    errno_photo_path = 'fotos/erno.jpg'


    if callback_query.data == 'cancel':
        ID = callback_query.from_user.id
        link = f'https://t.me/{BOT_NICKNAME}?start={ID}h'

        markup = InlineKeyboardBuilder()
        markup.add(
            InlineKeyboardButton(text="💌 Отправить ссылку",
                                 switch_inline_query=f"🥺 Отправь мне сообщение:\n\n {link}")
        )


        await state.clear()
        await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                                  caption=f'✅❌ <b>Отпрака сообщения отменена...</b>\n\n'
                                                          f'<b>Твоя ссылкa для вопросов:</b>\n'
                                                          f'{link}', parse_mode='html', reply_markup=markup.as_markup())
        return
    else:
        await callback_query.message.answer_photo(photo=FSInputFile(errno_photo_path), caption='❌ <b>Ошибка, пожалуйста, введите сообщение для получателя или нажмите отменить:</b>', parse_mode='html', reply_markup=cancel_keyboard())


@dp.message(Send.send)
async def answer(message: Message, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    new_mes_photo_path = 'fotos/message.jpg'
    message_for_user = message.text
    sender = db.get_sender2(message.from_user.id)
    await state.clear()
    await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'<b>✅ Ваше сообщение успешно отправлено! Ваше сообщение:</b>\n\n'
                                                                             f'<i>{message_for_user}</i>', parse_mode='html')
    await bot.send_photo(photo=FSInputFile(new_mes_photo_path), chat_id=sender,
                         caption=f'💌 <b>Новое сообщение для тебя:</b>\n\n'
                                 f'<i>{message_for_user}</i>', parse_mode='html', reply_markup=return_keyboard())


@dp.callback_query(lambda F: F.data == 'answer_user')
async def answer_user(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Введите ваш ответ на вопрос:', parse_mode='html', reply_markup=cancel_keyboard())
    await state.set_state(Send.send_answer)


@dp.message(Send.send_answer)
async def answer_answer(message: Message, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    new_mes_photo_path = 'fotos/message.jpg'


    message_for_user_answer = message.text
    sender = db.get_sender2(message.from_user.id)
    await state.clear()
    await message.answer_photo(photo=FSInputFile(success_photo_path),
                               caption=f'<b>✅ Ваш ответ на вопрос успешно отправлен! Ваш ответ:</b>\n\n'
                                       f'<i>{message_for_user_answer}</i>', parse_mode='html')

    await bot.send_photo(photo=FSInputFile(new_mes_photo_path), chat_id=sender,
                         caption=f'💌 <b>Новое сообщение для тебя (ответ на твой вопрос):</b>\n\n'
                                 f'<i>{message_for_user_answer}</i>', parse_mode='html')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
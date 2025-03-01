from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from db import Database
from keyboards import cancel_keyboard, return_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State



bot = Bot(token='7783210062:AAFC_H7lRdIPdcSrdbII_ETa0PY1pcTM25M')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database('database.db')

class Send(StatesGroup):
    send = State()
    send_answer = State()


@dp.message_handler(commands=['start'])
async def start(message: Message, state: FSMContext):
    question_photo_path = 'fotos/anonimous_q.jpg'
    ID = message.from_user.id
    start_command = message.text
    refferer = start_command[7:]
    print(refferer)
    ref_link = f'https://t.me/ultra_parcer_robot?start={ID}h'

    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="💌 Отправить ссылку",
                                  switch_inline_query=f"🥺 Отправь мне сообщение:\n\n {ref_link}")
    markup.add(button)

    # if 'h' in str(refferer):
    #     refferer_new = str(refferer).replace('h', '')
    #     print(refferer_new)

    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.username)
        db.set_signup(message.from_user.id, 'done')
        await message.answer_photo(photo=open(question_photo_path, "rb"),
                                   caption=f'<b>Привет, {message.from_user.first_name}, это бот анонимных вопросов!</b>\n\n'
                                           f'<b>Твоя ссылкa для вопросов:</b>\n'
                                           f'{ref_link}\n\n'
                                           f'Покажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!',
                                   parse_mode='html', reply_markup=markup)

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
            await message.answer('Введите ваш вопрос:', parse_mode='html', reply_markup=cancel_keyboard)
            await state.set_state(Send.send)
        else:
            await message.answer_photo(photo=open(question_photo_path, "rb"),
                                   caption=f'<b>Привет, {message.from_user.first_name}, это бот анонимных вопросов!</b>\n\n'
                                           f'<b>Твоя ссылкa для вопросов:</b>\n'
                                           f'{ref_link}\n\n'
                                           f'Покажи эту ссылку друзьям и подписчикам и получай от них анонимные вопросы и отвечай!',
                                   parse_mode='html', reply_markup=markup)


@dp.callback_query_handler(state=Send.send)
async def cancel_action(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'cancel':
        success_photo_path = 'fotos/success.jpg'
        ID = callback_query.from_user.id
        link = f'https://t.me/ultra_parcer_robot?start={ID}h'
        await state.finish()
        await callback_query.message.answer_photo(photo=open(success_photo_path, "rb"),
                                                  caption=f'✅❌ <b>Отпрака сообщения отменена...</b>\n\n'
                                                          f'<b>Твоя ссылкa для вопросов:</b>\n'
                                                          f'{link}', parse_mode='html')
        return
    else:
        errno_photo_path = 'fotos/erno.jpg'
        await callback_query.message.answer_photo(photo=open(errno_photo_path, "rb"), caption='❌ <b>Ошибка, пожалуйста, введите сообщение для получателя или нажмите отменить:</b>', parse_mode='html', reply_markup=cancel_keyboard)


@dp.message_handler(state=Send.send)
async def answer(message: Message, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    new_mes_photo_path = 'fotos/message.jpg'
    message_for_user = message.text
    sender = db.get_sender2(message.from_user.id)
    await state.finish()
    await message.answer_photo(photo=open(success_photo_path, "rb"), caption=f'<b>✅ Ваше сообщение успешно отправлено! Ваше сообщение:</b>\n\n'
                                                                             f'<i>{message_for_user}</i>', parse_mode='html')
    await bot.send_photo(photo=open(new_mes_photo_path, "rb"), chat_id=sender,
                         caption=f'💌 <b>Новое сообщение для тебя:</b>\n\n'
                                 f'<i>{message_for_user}</i>', parse_mode='html', reply_markup=return_keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'answer_user')
async def answer_user(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Введите ваш ответ на вопрос:', parse_mode='html', reply_markup=cancel_keyboard)
    await state.set_state(Send.send_answer)


@dp.message_handler(state=Send.send_answer)
async def answer_answer(message: Message, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    new_mes_photo_path = 'fotos/message.jpg'
    message_for_user_answer = message.text
    sender = db.get_sender2(message.from_user.id)
    await state.finish()
    await message.answer_photo(photo=open(success_photo_path, "rb"),
                               caption=f'<b>✅ Ваш ответ на вопрос успешно отправлен! Ваш ответ:</b>\n\n'
                                       f'<i>{message_for_user_answer}</i>', parse_mode='html')
    await bot.send_photo(photo=open(new_mes_photo_path, "rb"), chat_id=sender,
                         caption=f'💌 <b>Новое сообщение для тебя (ответ на твой вопрос):</b>\n\n'
                                 f'<i>{message_for_user_answer}</i>', parse_mode='html')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
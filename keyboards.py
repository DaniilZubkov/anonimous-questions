from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder


def cancel_keyboard():
   builder = Builder()
   builder.add(
      InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'),
   )
   return builder.as_markup()



def return_keyboard():
   builder = Builder()
   builder.add(
      InlineKeyboardButton(text='💥 Ответить', callback_data='answer_user'),
   )
   return builder.as_markup()
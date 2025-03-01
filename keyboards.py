from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[(
   InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'),
)])

return_keyboard = InlineKeyboardMarkup(inline_keyboard=[(
   InlineKeyboardButton(text='💥 Ответить', callback_data='answer_user'),
)])
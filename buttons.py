from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


sizes = ReplyKeyboardMarkup().add(
    KeyboardButton(text='XL'),
    KeyboardButton(text='M'),
    KeyboardButton(text='L')
)

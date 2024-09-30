from urllib.request import urlcleanup
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


sizes = ReplyKeyboardMarkup().add(
    KeyboardButton(text='XL'),
    KeyboardButton(text='M'),
    KeyboardButton(text='L')
)

link = 'https://online.geeks.kg/'
web=types.WebAppInfo(url=link)
urls=types.InlineKeyboardMarkup(types.InlineKeyboardButton(text='geeks',web_app=web))

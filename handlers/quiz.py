from config import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def question1(message: types.Message):
    murkup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='next', callback_data='next1')
    murkup.add(b1)

    q = 'Mercedes or BMW'
    v = ['Mercedes', 'BMW']
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=q,
        options=v,
        type='quiz',
        is_anonymous=False,
        correct_option_id=1,
        explanation='ахахах',
        reply_markup=murkup
    )


async def question2(call: types.CallbackQuery):
    murkup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='next', callback_data='next2 ')

    q = 'Ronaldo or Messi'
    v = ['Ronaldo', 'Messi']
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=q,
        options=v,
        type='quiz',
        is_anonymous=False,
        correct_option_id=1,
        explanation='ахахах',
        reply_markup=murkup
    )


async def question3(call: types.CallbackQuery):
    murkup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='next', callback_data='next2 ')

    q = 'j or k'
    v = ['j', 'k']
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=q,
        options=v,
        type='quiz',
        is_anonymous=False,
        correct_option_id=1,
        explanation='ахахах',
    )

def register_quiz(dp: Dispatcher):
    dp.register_message_handler(question1, commands=['quiz '])
    dp.callback_query_handler(question2, text='next1')
    dp.register_callback_query_handler(question3, text='next2 ')
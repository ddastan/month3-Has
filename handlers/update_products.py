import sqlite3
from itertools import product
from unicodedata import category

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class EditProducts(StatesGroup):
    waiting_for_field = State()
    waiting_for_new_value = State()
    waiting_for_new_photo = State()


def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM products p
    INNER JOIN products detail pd ON p.product_id = pd.product_id
    """).fetchall()
    conn.close()
    return products

def update_products_field(product_id, field_name, name_value):
    products_table = ['name_products', 'size', 'price', 'photo']
    products_detail_table = ['category', 'info_product']

    conn = get_db_connection()

    try:
        if field_name in products_table:
            query = f"UPDATE products SET {field_name} = ? WHERE product_id = ?"
        elif field_name in products_detail_table:
            query = f"UPDATE products_detail SET {field_name} = ? WHERE product_id = ?"
        else:
            raise ValueError(f'Недопустимое имя поля:{field_name}')

    except sqlite3.OperationalError as e:
        print(f'Ошибка {e}')
    finally:
        conn.close()



async def start_sending_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    buttton = InlineKeyboardButton('Посмотреть', callback_data='show_all_updates')
    keyboard.add(buttton)

    await message.answer('Нажми на кнопку для отправки всех товаров!', reply_markup=keyboard)

async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            button = InlineKeyboardButton('Редактировать', callback_data=f'edit_{product["product_id"]}')
            keyboard.add(button)

            caption = (f'Артикул - {product["product_id"]}\n'
                       f'Название - {product["name_product"]}\n'
                       f'Информация - {product["info_product"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Цена - {product["price"]} com \n')

            await callback_query.message.answer_photo(photo=product['photo'], caption=caption, reply_markup=keyboard)


    else:
        await callback_query.message.answer('Товары не найдены')


async def edit_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]

    await state.update_data(product_id=product_id)

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    name_button = InlineKeyboardButton(text='Название', callback_data='field_name_product')
    category_button = InlineKeyboardButton(text='Категория', callback_data='field_category')



def register_update_product_handler(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products_update'])



from aiogram import types, Dispatcher
from config import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import sizes

class FSM_store(StatesGroup):
    name=State()
    size=State()
    category=State()
    price=State()
    photo=()


async def fsm_start(message: types.Message):
    await message.answer('name of product?:')
    await FSM_store.name.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
    await message.answer('size of product?:', reply_markup=sizes)
    await FSM_store.next()

async def load_size(message: types.Message, state:FSMContext):
    if message.text in sizes:
        async with state.proxy() as data:
            data['size'] = message.text
        await message.answer('category of product?:', reply_markup=types.ReplyKeyboardRemove())
        await FSM_store.next()
    else:
        await message.answer('press buttons')

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category']=message.text
    await message.answer('price of product?:')
    await FSM_store.next()

async def load_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['price'] = message.text
        await message.answer('photo of product?:')
        await FSM_store.next()
    else:
        await message.answer('only digits!!!')


async def load_photo(message: types.Message, state:FSMContext):
    photo=message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo']=photo
    await message.answer_photo(photo=photo,
                               caption=f'name: {data["name"]}\n'
                                       f'size: {data["size"]}\n'
                                       f'category: {data["category"]}\n'
                                       f'price: {data["price"]}')

    await state.finish()


def register_fsm_store(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['register_prod'])
    dp.register_message_handler(load_name, state=FSM_store.name)
    dp.register_message_handler(load_size, state=FSM_store.size)
    dp.register_message_handler(load_category, state=FSM_store.category)
    dp.register_message_handler(load_price, state=FSM_store.price)
    dp.register_message_handler(load_photo, state=FSM_store.photo, content_types=['photo'])







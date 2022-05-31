from aiogram import types

from context import dp

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    pass

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    pass

@dp.message_handler(commands=["duty"])
async def duty(message: types.Message):
    pass

@dp.message_handler(commands=["alarm"])
async def alarm(message: types.Message):
    pass

@dp.message_handler(commands=["wash"])
async def wash(message: types.Message):
    pass

@dp.message_handler(commands=["kitchen"])
async def kitchen(message: types.Message):
    pass


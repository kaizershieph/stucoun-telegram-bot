from curses.ascii import FS
from aiogram import types
from aiogram.dispatcher import FSMContext

from context import dp
from misc.states import AlarmStates, WashStates

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
async def raise_alarm(message: types.Message):
    pass

@dp.message_handler(state=AlarmStates.RaiseAlarm)
async def confirm_alarm(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(commands=["wash"])
async def view_wash(message: types.Message):
    pass

@dp.message_handler(state=WashStates.AddWash)
async def add_wash(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(state=WashStates.EnterDateWash)
async def enter_date_wash(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(state=WashStates.EnterHourWash)
async def enter_hour_wash(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(state=WashStates.ConfirmNewWash)
async def confirm_new_wash(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(commands=["kitchen"])
async def kitchen(message: types.Message):
    pass


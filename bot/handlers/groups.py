import datetime as dt

from aiogram import types
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from tortoise.expressions import Q

from context import dp
from bot.database.models import *
from bot.templates.messages import *


@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), commands=["start"])
async def start_message(message: types.Message):
    await message.answer(text=str(StartMessage))

@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), commands=["help"])
async def help(message: types.Message):
    await message.answer(text=str(HelpMessage))

@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), commands=["duty"])
async def duty(message: types.Message):
    today = dt.date.today()
    staff = await DutyTimetable.filter(date=today)\
        .prefetch_related().values('staff__name','staff__phone')[0]
    await message.answer(text=str(DutyMessage(staff['staff__name'], staff['staff__phone'])))
    

@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), commands=["wash"])
async def wash(message: types.Message):
    today = dt.date.today()
    today_timetable = await WashTimetable.filter(date=today).order_by('time').values_list('time','room')
    await message.answer(
        text=str(WashDayTimetableMessage(
            date=today,
            appointments=list([WashAppointment(t,r) for t,r in today_timetable])
            )) + f'Посмотреть расписание на неделю и записаться: <a href="{TELEGRAM_URL}{BOT_NAME}">открыть чат</a>'
        )


@dp.message_handler(ChatTypeFilter(types.ChatType.GROUP), commands=["kitchen"])
async def kitchen(message: types.Message):
    today = dt.date.today()
    week = list([x for x in [today + dt.timedelta(days=n) for n in range(8)]])
    week_timetable = await KitchenTimetable.filter(Q(date__in=week)).order_by('date', 'room')\
        .values_list('date', 'room')
    await message.answer(
        text=str(KitchenTimetableMessage(
            appointments=list([KitchenAppointment(d, r) for d,r in week_timetable])
        ))
    )


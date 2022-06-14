import asyncio
import datetime as dt
from tkinter import W

from tortoise.expressions import Q

from bot.services.services import repeatting
from bot.database.models import WashTimetable, KitchenTimetable, Groups
from context import dp, config


@repeatting(hours=24)
async def prepare_wash_timetable():
    today = dt.date.today()
    await WashTimetable.filter(Q(date__lt=today)).delete()
    midnight = dt.time.fromisoformat('00:00')
    await WashTimetable.create(
        date=today + dt.timedelta(days=7), 
        time__in=list([midnight + dt.timedelta(hours=n) for n in range(24)]),
        room=None
        )
    await WashTimetable.save()

@repeatting(hours=24)
async def notify_kitchen_duty():
    today = dt.date.today()
    kitchen_duty = await KitchenTimetable.filter(date=today).values_list('room')
    repr = ','.join(kitchen_duty)
    await dp.bot.send_message(
        chat_id=config.bot.group_id,
        text=f'Напоминаю, что сегодня на кухнях дежурят комнаты: <code>{repr}</code>'
        )

#TODO

import datetime as dt

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from tortoise.expressions import Q

from bot.context import dp
from bot.templates.messages import *
from bot.templates.keyboards import *
from bot.database.models import *
from misc.states import WashStates


DATE_INDICATORS = [str(n) for n in range(10)] + ['.']


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["start"])
async def start_message(message: types.Message):
    await message.answer(text=str(StartMessage))

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["help"])
async def help(message: types.Message):
    await message.answer(text=str(HelpMessage))

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["duty"])
async def duty(message: types.Message):
    today = dt.date.today()
    staff = await DutyTimetable.filter(date=today)\
        .prefetch_related().values('staff__name','staff__phone')[0]
    await message.answer(text=str(DutyMessage(staff['staff__name'], staff['staff__phone'])))


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["wash"])
async def view_wash(message: types.Message):
    today = dt.date.today()
    today_timetable = await WashTimetable.filter(date=today).order_by('time').values_list('time','room')
    await message.answer(
        text=str(WashDayTimetableMessage(
            date=today,
            appointments=list([WashAppointment(t,r) for t,r in today_timetable])
            )),
        reply_markup=wash_info_markup
        )
    await WashStates.first()

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text='Отмена', state=WashStates.all_states)
async def cancel(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.delete()

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text='Новая запись', state=WashStates.AddWash)
async def add_wash(message: types.Message, state: FSMContext):
    today = dt.date.today()
    week = list([x for x in [today + dt.timedelta(days=n) for n in range(8)]])
    await WashStates.next()
    await message.answer(text='Отлично! Выбери день недели:',  reply_markup=WashWeekMarkup(week))

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text=Text(contains=DATE_INDICATORS),state=WashStates.EnterDateWash)
async def enter_date_wash(message: types.Message, state: FSMContext):
    parts = message.text.split()
    text = parts[0] if len(parts) < 2 else parts[1]
    iso = f'{str(dt.date.today().year)}-{text[-2:]}-{text[:3]}'

    try:
        date = dt.date.fromisoformat(iso)
        day_timetable = await WashTimetable.filter(date=date).order_by('date').values_list('time', 'room')
        free = list([(_,r) for _,r in day_timetable if r is None])
        await state.update_data({'date': date})
        await WashStates.next()
        await message.answer(
            text=str(WashDayTimetableMessage(
                date=date,
                appointments=list([WashAppointment(t, r) for t,r in day_timetable])
                )),
                reply_markup=WashNewAppointmentMarkup(free).build_markup()
            )
    except:
        await message.answer(text='Неверный формат даты. Попробуй DD.MM или нажми на кнопку')

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text=Text(contains=':'), state=WashStates.EnterHourWash)
async def enter_hour_wash(message: types.Message, state: FSMContext):
    time = dt.time.fromisoformat(message.text)
    await state.update_data({'time': time})
    await WashStates.next()
    await message.answer(
        text='Введи номер комнаты. Например: <i>207</i>')

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text=Text(contains=[str(n) for n in range(10)]), state=WashStates.EnterRoomWash)
async def enter_room_wash(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        number = ''
        for c in message.text:
            if c.isdigit():
                number += c
    else:
        number = message.text
    
    await state.update_data({'room': number})
    await WashStates.next()

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=WashStates.SummaryWash)
async def summary_confirm_wash(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await WashStates.next()
    await message.answer(
        text=str(WashAppointmentConfirmMessage(**data)),
        reply_markup=wash_appointment_confirm_markup
        )

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), text='Подтвердить', state=WashStates.ConfirmNewWash)
async def confirmed_new_wash(message: types.Message, state: FSMContext):
    await WashTimetable.filter(
        date=state.get_data('date'), 
        time=state.get_data('time')
        ).update({'room': state.get_data('room')})
    await WashTimetable.save()
    await state.finish()
    await message.answer('Успешно!')


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=["kitchen"])
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
    



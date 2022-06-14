from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


alarm_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сообщить'),
            KeyboardButton(text='Отмена')
        ]
    ]
)

wash_info_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новая запись')
        ]
    ]
)

class WashWeekMarkup:

    def __init__(self, week) -> None:
        self.week = week

    def build_markup(self):
        markup = list([
            KeyboardButton(text=day.strftime("%a %d.%m")) for day in self.week
        ]) + [KeyboardButton(text='Отмена')]
        
        return ReplyKeyboardMarkup(keyboard=markup)


class WashNewAppointmentMarkup:

    def __init__(self, records) -> None:
        self.records = records

    def build_markup(self):
        markup = list([
            KeyboardButton(text=time.strftime("%H:%M")) for time in self.records
        ]) + [KeyboardButton(text='Отмена')]

        return ReplyKeyboardMarkup(keyboard=markup)


wash_appointment_confirm_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить'),
            KeyboardButton(text='Отмена')
        ]
    ]
)

    
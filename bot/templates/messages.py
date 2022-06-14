from datetime import date, time

TELEGRAM_URL = 'https://t.me/'
BOT_NAME = 'stucoun_bot'


class StartMessage:

    def __repr__(self) -> str:
        return '\n'.join([
            'Привет, я бот-помощник <b>Stucoun</b>!\n',
            'Моя задача — облегчить работу студсовета в общежитии. Я знаю кто сегодня дежурная, веду расписания стирок и уборок на кухне, сообщаю о важных событиях в общежитии и еще много чего.\n',
            'Чтобы узнать о поддерживаемых мной командах, введи <code>/help</code>'
        ])


class HelpMessage:

    def __repr__(self) -> str:
        return '\n'.join([
            'Для взаимодействия со мной нужно использовать специальные команды.\n',
            'Вот список команд с кратким описанием каждой:\n',
            '<code>/duty</code> — <i>узнать кто из администрации сегодня на дежурстве</i>',
            '<code>/wash</code> — <i>узнать актуальное расписание постирочной комнаты, а также записаться на стирку</i>',
            '<code>/kitchen</code> — <i>узнать расписание дежурств на кухне в течение недели</i>',
            '<code>/alarm</code> — <i>сообщить администрации и проживающим о возникшей чрезвычайной ситуации</i>\n',
            'Скорее, напиши мне по любому интересующему тебя вопросу!'
        ])


class DutyMessage:

    def __init__(self, name, phone) -> None:
        self.name = name
        self.phone = phone

    def __repr__(self) -> str:
        return '\n'.join([
            f'Сегодня в общежитии дежурит <b>{self.name}</b>\n',
            f'Позвонить: <code>{self.phone}</code>',
            f'Написать: <a href="{TELEGRAM_URL}{self.phone}">открыть чат</a>'
        ]) 
        

class WashPickDayMessage:

    def __repr__(self) -> str:
        return '\n'.join([
            'Выбери день'
        ])


class WashAppointment:
    
    def __init__(self, time, room) -> None:
        self.time = time
        self.room = room or 'FREE'
    
    def __repr__(self) -> str:
        return f'<i>{self.time.strfo}</i> — <code>{self.room}</code>'


class WashDayTimetableMessage:

    def __init__(self, date, appointments) -> None:
        self.date = date
        self.appointments = appointments

    def __repr__(self) -> str:
        timetable_list = '\n'.join([str(a) for a in self.appointments])
        return '\n'.join([
            f'<b>Расписание стирок на {self.date.strftime("%a %d.%m")}</b>\n\n',
            timetable_list,
        ])


class WashAppointmentConfirmMessage:

    def __init__(self, date, time, room) -> None:
        self.date = date
        self.time = time
        self.room = room

    def __repr__(self) -> str:
        return '\n'.join([
            f'Выбрана дата: <i>{self.date.strftime("%a %d.%m")}</i>',
            f'Выбрано время: <i>{self.time.strftime("%H:%M")}</i>'
            f'Номер комнаты: <code>{self.room}</code>'
        ])


class KitchenAppointment:

    def __init__(self, date, room) -> None:
        self.date = date
        self.room = room

    def __repr__(self) -> str:
        return f'<i>{self.date.strftime("%a %d.%m")}</i> — <code>{self.room}</code>'


class KitchenTimetableMessage:

    def __init__(self, appointments) -> None:
        self.appointments = appointments

    def __repr__(self) -> str:
        timetable_list = '\n'.join([str(a) for a in self.appointments])
        return '\n'.join([
            '<b>Расписание дежурств на кухне</b>\n',
            timetable_list,
        ])



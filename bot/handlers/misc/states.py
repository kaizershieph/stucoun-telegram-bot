from aiogram.dispatcher.filters.state import StatesGroup, State

class AlarmStates(StatesGroup):
    RaiseAlarm = State()
    ConfirmAlarm = State()


class WashStates(StatesGroup):
    ViewWash = State()
    AddWash = State()
    EnterDateWash = State()
    EnterHourWash = State()
    EnterRoomWash = State()
    SummaryWash = State()
    ConfirmNewWash = State()

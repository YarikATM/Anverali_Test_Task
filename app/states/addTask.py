from aiogram.fsm.state import StatesGroup, State


class addTaskState(StatesGroup):
    choosing_title = State()
    choosing_desc = State()
    choosing_date = State()
    confirm = State()



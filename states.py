from aiogram.fsm.state import State, StatesGroup


class Prices(StatesGroup):
    china = State()
    usa = State()
from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    START = State()
    ENTER_NAME = State()
    CHOOSE_FILE = State()
    CHOOSE_DELIVERY = State()
    ASKING_EMAIL = State()
from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeNewsletter(StatesGroup):
    get_text = State()
    get_attached = State()
    get_button = State()
    get_count = State()
    get_channels = State()

    edit_text = State()
    edit_attached = State()
    edit_button = State()
    edit_count = State()
    edit_channels = State()

    changes = State()

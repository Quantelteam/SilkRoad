from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    program = State()
    number = State()
    name = State()
    city = State()
    join = State()


class NewListing(StatesGroup):
    type = State()
    part = State()      # part picker (see handlers/parts_picker.py)
    price = State()
    condition = State()
    photos = State()
    note = State()
    confirm = State()


class EditListing(StatesGroup):
    menu = State()
    part = State()
    price = State()
    condition = State()
    note = State()
    photos = State()

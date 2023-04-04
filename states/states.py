from telebot.handler_backends import State, StatesGroup


class MyState(StatesGroup):
    code = State()
    lang = State()


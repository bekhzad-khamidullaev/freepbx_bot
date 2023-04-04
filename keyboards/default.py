from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def btn_default():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(text='📞️ Звонки сегодня'), KeyboardButton(text='🗓 Выбрать дату'))
    markup.add(KeyboardButton(text='🔎 Поиск по номеру'))
    return markup

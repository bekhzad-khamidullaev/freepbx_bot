from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


# MAIN BUTTONS
def btn_calls(data_type, to_date, offset, phone=None):
    markup = InlineKeyboardMarkup(row_width=2)
    button_0 = InlineKeyboardButton(text= '☎️ Пропущенные', callback_data=f"{data_type}|missed|{to_date}|{offset}|{phone}")
    button_1 = InlineKeyboardButton(text='⬇️ Входяшие', callback_data=f"{data_type}|in|{to_date}|{offset}|{phone}")
    button_2 = InlineKeyboardButton(text='⬆️ Исходяшие', callback_data=f"{data_type}|out|{to_date}|{offset}|{phone}")
    button_3 = InlineKeyboardButton(text='#️⃣  Закрыть', callback_data="close")
    markup.add(button_1, button_2)
    markup.add(button_3)
    return markup


def btn_calls_for_phone(phone):
    markup = InlineKeyboardMarkup(row_width=2)
    button_0 = InlineKeyboardButton(text= '☎️ Пропущенные', callback_data=f"phone|missed|{phone}|0")
    button_1 = InlineKeyboardButton(text='⬇️ Входяшие', callback_data=f"phone|in|{phone}|0")
    button_2 = InlineKeyboardButton(text='⬆️ Исходяшие', callback_data=f"phone|out|{phone}|0")
    button_3 = InlineKeyboardButton(text='#️⃣  Закрыть', callback_data="close")
    markup.add(button_0)
    markup.add(button_1, button_2)
    markup.add(button_3)
    return markup


def btn_pagination(data_type, direction, to_date, offset, total_calls, MESS_MAX):
    markup = InlineKeyboardMarkup(row_width=2)
    if total_calls > MESS_MAX:

        next_page = MESS_MAX + offset
        first_page = 0

        if next_page >= total_calls:
            button_1 = InlineKeyboardButton(text='⬅️', callback_data=f"{data_type}|{direction}|{to_date}|{first_page}")
            markup.add(button_1)
        else:
            next_page = MESS_MAX + offset
            button_2 = InlineKeyboardButton(text='➡️', callback_data=f"{data_type}|{direction}|{to_date}|{next_page}")
            markup.add(button_2)

        # else:
        #     button_1 = InlineKeyboardButton(text='⬅️', callback_data=f"{data_type}|{direction}|{to_date}|{previous_page}")
        #     button_2 = InlineKeyboardButton(text='➡️', callback_data=f"{data_type}|{direction}|{to_date}|{next_page}")
        #     markup.add(button_1, button_2)

        button_3 = InlineKeyboardButton(text='#️⃣  Закрыть', callback_data="close")
    else:
        button_3 = InlineKeyboardButton(text='#️⃣  Закрыть', callback_data="close")
    markup.add(button_3)
    return markup


def btn_generate_numbers():
    markup = InlineKeyboardMarkup(row_width=3)
    number_1 = InlineKeyboardButton(text='1', callback_data="number|1")
    number_2 = InlineKeyboardButton(text='2', callback_data="number|2")
    number_3 = InlineKeyboardButton(text='3', callback_data="number|3")
    number_4 = InlineKeyboardButton(text='4', callback_data="number|4")
    number_5 = InlineKeyboardButton(text='5', callback_data="number|5")
    number_6 = InlineKeyboardButton(text='6', callback_data="number|6")
    number_7 = InlineKeyboardButton(text='7', callback_data="number|7")
    number_8 = InlineKeyboardButton(text='8', callback_data="number|8")
    number_9 = InlineKeyboardButton(text='9', callback_data="number|9")
    number_0 = InlineKeyboardButton(text='0', callback_data="number|0")
    confirm = InlineKeyboardButton(text='✅', callback_data="number|yes")
    clear = InlineKeyboardButton(text='❌', callback_data="number|clear")
    close = InlineKeyboardButton(text='#️⃣  Закрыть', callback_data="close")
    markup.add(number_1, number_2, number_3)
    markup.add(number_4, number_5, number_6)
    markup.add(number_7, number_8, number_9)
    markup.add(clear, number_0, confirm)
    markup.add(close)
    return markup
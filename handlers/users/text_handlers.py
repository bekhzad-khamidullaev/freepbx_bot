import os
from datetime import datetime

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from data.loader import bot
from database.database import *
from keyboards.inline import *
from states.states import MyState


@bot.message_handler(regexp='📞️ Звонки сегодня', chat_types='private')
def calls_today(message):
    chat_id = message.from_user.id
    now = datetime.datetime.now()
    data_type = 'call'
    offset = 0
    to_date = now.date()
    msg = f'Звонки на {to_date}:'
    bot.send_message(chat_id, msg, reply_markup=btn_calls(data_type, to_date, offset))


@bot.message_handler(regexp='🗓 Выбрать дату', chat_types='private')
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        to_date = result
        data_type = 'call'
        offset = 0
        bot.edit_message_text(f"Звонки на {to_date}:",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=btn_calls(data_type, to_date, offset))


@bot.message_handler(regexp='🔎 Поиск по номеру', chat_types='private')
def calls_to_date(message):
    chat_id = message.from_user.id
    bot.set_state(chat_id, MyState.code, chat_id)
    with bot.retrieve_data(chat_id, chat_id) as data:
        data['code'] = []
    bot.send_message(chat_id, 'Введите 9 знаков телефонного номера: ', reply_markup=btn_generate_numbers())



@bot.message_handler(func=lambda msg: msg.text[0] == '/')
def get_id(message):
    chat_id = message.from_user.id
    id_ = message.text[1:]
    uniqueid = f"{id_}%"
    file = get_get_file_from_unique_id(uniqueid)
    recordingfile = file['recordingfile']
    t1 = file['calldate']
    year = str("{:04d}".format(t1.year))
    month = str("{:02d}".format(t1.month))
    day = str("{:02d}".format(t1.day))
    true_path = '/var/spool/asterisk/monitor/'
    records_path = os.path.join(true_path)
    document = str(records_path + year + '/' + month + '/' + day + '/' + recordingfile)
    doc = open(document, 'rb')
    bot.send_document(chat_id, doc, caption=file['calldate'])



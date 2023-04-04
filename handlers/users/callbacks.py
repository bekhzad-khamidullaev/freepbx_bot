import os

from telebot.types import CallbackQuery

from data.loader import bot
from database.database import *
from keyboards.default import *
from keyboards.inline import *

true_path = '/var/spool/asterisk/monitor/'
records_path = os.path.join(true_path)

MESS_MAX = 10


@bot.callback_query_handler(func=lambda call: 'call' in call.data)
def reaction_to_in_out(call: CallbackQuery):
    data_type = call.data.split('|')[0]
    direction = call.data.split('|')[1]
    to_date = call.data.split('|')[2]
    offset = int(call.data.split('|')[3])
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)

    if direction == 'in':
        dcontext = 'ext-queues'
        direction_text = 'Входящие звонки'
    else:
        dcontext = 'from-internal'
        direction_text = 'Исходящие звонки'

    d_from = f'{to_date} 00:00:00'
    d_to = f'{to_date} 23:59:59'

    all_calls = get_records(d_from, d_to, dcontext, MESS_MAX, offset)
    total_calls = get_total_records(d_from, d_to, dcontext)

    if all_calls:
        msg = f'Тип: {direction_text} \nДата: {to_date} \nКоличетсво:  <b>{len(total_calls)}</b> \n\n'
        a = offset
        for call_data in all_calls:
            a += 1

            t1 = call_data['calldate']
            t2 = "%s:%s" % (t1.hour, t1.minute)
            d1 = call_data['duration'] // 60
            if d1 == 0:
                d2 = f"{call_data['duration']} сек."
            else:
                d2 = f"{d1} мин."

            unique_id = call_data['uniqueid'].split('.')[0]

            if call_data['dcontext'] == 'from-internal':
                s1 = call_data['channel'].split('/')[1]
                src = s1.split('-')[0]
                msg += f"{a}) {t2} *️⃣  <b>{src} ➡️ {call_data['dst']}</b> \n  🕒{d2} ⬇️️/{unique_id} \n\n"

            elif call_data['dcontext'] == 'ext-queues':
                try:
                    d1 = call_data['dstchannel'].split('/')[1]
                except:
                    d1 = call_data['dstchannel']

                dst = d1.split('@')[0]
                msg += f"{a}) {t2} * <b>{call_data['src']} ➡️ {dst}</b> \n🕒{d2} ☑️/{unique_id} \n\n"

        bot.send_message(user_id, f"{msg}", parse_mode='HTML', reply_markup=btn_pagination(data_type, direction, to_date, offset, len(total_calls), MESS_MAX))
        # bot.send_message(user_id, f"{msg}", parse_mode='HTML')

    else:
        bot.send_message(user_id, "На выбранную дату записи не найдены", reply_markup=btn_default())


@bot.callback_query_handler(func=lambda call: 'phone' in call.data)
def reaction_to_in_out(call: CallbackQuery):
    print(call.data)
    data_type = call.data.split('|')[0]
    direction = call.data.split('|')[1]
    offset = int(call.data.split('|')[3])
    phone = call.data.split('|')[2]
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)

    if direction == 'in':
        dcontext = 'ext-queues'
        direction_text = 'Входящие звонки'
        all_calls = get_records_phone_in(phone, dcontext, MESS_MAX, offset)
        total_calls = get_total_records_phone_in(phone, dcontext)
    else:
        dcontext = 'from-internal'
        direction_text = 'Исходящие звонки'
        all_calls = get_records_phone_out(phone, dcontext, MESS_MAX, offset)
        total_calls = get_total_records_phone_out(phone, dcontext)



    if all_calls:
        msg = f'Тип: {direction_text} \nНомер: {phone} \nКоличетсво:  <b>{len(total_calls)}</b> \n\n'
        a = offset
        for call_data in all_calls:
            a += 1

            t1 = call_data['calldate']
            t2 = "%s:%s" % (t1.hour, t1.minute)
            d1 = call_data['duration'] // 60
            if d1 == 0:
                d2 = f"{call_data['duration']} сек."
            else:
                d2 = f"{d1} мин."

            unique_id = call_data['uniqueid'].split('.')[0]

            if call_data['dcontext'] == 'from-internal':
                s1 = call_data['channel'].split('/')[1]
                src = s1.split('-')[0]
                msg += f"{a}) {call_data['calldate']} \n*️⃣  <b>{src} ➡️ {call_data['dst']}</b> \n  🕒{d2} ⬇️️/{unique_id} \n\n"

            elif call_data['dcontext'] == 'ext-queues':
                try:
                    d1 = call_data['dstchannel'].split('/')[1]
                except:
                    d1 = call_data['dstchannel']

                dst = d1.split('@')[0]
                msg += f"{a}) {call_data['calldate']} \n*️⃣  <b>{call_data['src']} ➡️ {dst}</b> \n🕒{d2} ⬇️️/{unique_id} \n\n"

        bot.send_message(user_id, f"{msg}", parse_mode='HTML', reply_markup=btn_pagination(data_type, direction, phone, offset, len(total_calls), MESS_MAX))
        # bot.send_message(user_id, f"{msg}", parse_mode='HTML')

    else:
        bot.send_message(user_id, "Записи не найдены", reply_markup=btn_default())





@bot.callback_query_handler(func=lambda call: call.data == 'close')
def reaction_to_close(call: CallbackQuery):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: 'number|' in call.data)
def reaction_to_number(call: CallbackQuery):
    user_id = call.message.chat.id
    number = call.data.split('|')[1]
    with bot.retrieve_data(user_id, user_id) as data:
        if number == 'yes':
            try:
                x_code = ''.join(data['code'])
                if len(x_code) == 9:
                    bot.delete_message(user_id, call.message.message_id)
                    msg = f'Звонки на номер {x_code}:'
                    bot.answer_callback_query(call.id, msg)
                    bot.send_message(user_id, msg, reply_markup=btn_calls_for_phone(x_code))
                    data['code'] = []
                else:
                    data['code'] = []
                    bot.answer_callback_query(call.id, 'Не правильный номе телефона')
            except:
                data['code'] = []
                bot.answer_callback_query(call.id, 'Не правильный номе телефона')
        elif number == 'clear':
            data['code'] = []
            bot.answer_callback_query(call.id, 'Очищено')
        else:
            data['code'].append(number)
            x_code = ''.join(data['code'])
            bot.answer_callback_query(call.id, f"{x_code}")
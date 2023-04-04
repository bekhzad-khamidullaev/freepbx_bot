from telebot.types import Message

from data.loader import bot
from keyboards.default import *


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Asterisk", reply_markup=btn_default())

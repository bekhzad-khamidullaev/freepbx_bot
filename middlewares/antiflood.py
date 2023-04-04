from telebot.handler_backends import BaseMiddleware
from telebot.handler_backends import CancelUpdate
from telebot.types import ReplyKeyboardRemove

from data.loader import bot


class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        super().__init__()
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            bot.send_message(message.chat.id, 'To many attempts. Restart /start', reply_markup=ReplyKeyboardRemove())
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass
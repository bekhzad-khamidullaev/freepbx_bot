from telebot import TeleBot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
# from database.database import DataBase
from telebot.types import BotCommand

from config import TOKEN

state_storage = StateMemoryStorage()


bot = TeleBot(TOKEN, use_class_middlewares=True)

bot.set_my_commands(
    commands=[
        BotCommand('/start', 'Restart'),
    ]
)

bot.add_custom_filter(custom_filters.StateFilter(bot))
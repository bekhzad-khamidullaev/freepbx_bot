from datetime import time

from data.loader import bot

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as E:
            print(E)
            time.sleep(2)

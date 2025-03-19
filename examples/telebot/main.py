import uuid

from easy_di import BaseInjector
from handlers import router
from plugs import Bot

bot = Bot(uuid.uuid4())

def main():
    BaseInjector.register('bot', bot)
    bot.register(router)
    bot.start()


if __name__ == '__main__':
    main()
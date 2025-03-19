from easy_di import BaseInjector
from plugs import Router

router = Router()


@BaseInjector('bot')
def hi(deps):
    bot = deps['bot']
    bot.send(f"Hi I'm {bot.me()}")


router.register(hi)
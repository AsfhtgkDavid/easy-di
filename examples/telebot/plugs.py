class Bot:
    def __init__(self, token):
        self._token = token
        self._routers = []

    def send(self, message):
        print(f'Sending message: "{message}" to token: {self._token}')

    def me(self):
        return "daikabot"

    def register(self, router):
        self._routers.append(router)

    def start(self):
        for router in self._routers:
            router.handle()

class Router:
    def __init__(self):
        self._handlers = []

    def register(self, handler):
        self._handlers.append(handler)

    def handle(self):
        for handler in self._handlers:
            handler()
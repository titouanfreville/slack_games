from app.core import Context, Log


class Ping:
    def __init__(self, log: Log):
        self.__log = log.named("usecases.pings")

    def server_alive(self, ctx: Context) -> str:
        self.__log.context(ctx).method("server_alive").success()

        return "pong"

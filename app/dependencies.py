from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, Singleton
from dependency_injector.wiring import Provide

from app.routes import API

from ._dependencies import Core, Endpoints, Usecases


######### APPLICATION CONTAINERS #########
class SlackGames(DeclarativeContainer):
    config = Configuration()

    core: Core = Container(Core, config=config)  # type: ignore

    usecase: Usecases = Container(Usecases, core=core)  # type: ignore

    endpoints: Endpoints = Container(Endpoints, usecase=usecase)  # type: ignore

    # ----------------------------------------
    # Transports
    # ----------------------------------------
    router = Singleton(API, endpoints.pings)


######### IN APP SETUP #########
def setup_api_backgound(
    _log=Provide[SlackGames.core.logging],
):
    pass

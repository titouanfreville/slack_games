from app.routes import pings
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Singleton

from .usecases import Usecases


class Endpoints(DeclarativeContainer):
    usecase: Usecases = DependenciesContainer()  # type: ignore

    pings = Singleton(pings.Pings, usecase=usecase.pings)

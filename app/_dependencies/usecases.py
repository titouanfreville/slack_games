from app.domain import usecases
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Singleton

from .core import Core


class Usecases(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore

    pings = Singleton(usecases.Ping, core.logger)

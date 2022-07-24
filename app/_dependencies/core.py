import logging

from app.core import logger
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton


def _setup_logging(config) -> None:
    handlers = [logging.StreamHandler()]  # set default logger to console

    logging.basicConfig(
        format='{"level": "%(levelname)s", "name": "%(name)s", "at": "%(asctime)s", "message": %(message)s}',  # noqa: E501
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.getLevelName(config["log"]["level"]),
        force=True,
        handlers=handlers,
    )


class Core(DeclarativeContainer):
    config = Configuration()

    logging = Singleton(_setup_logging, config)
    # sentry = Singleton(_setup_sentry, config)
    # dramatiq = Singleton(_setup_dramatiq, config)

    logger = Factory(logger.Log, config)

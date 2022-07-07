from app.core import RestContext
from app.domain import usecases
from fastapi import APIRouter, Request


class Pings:
    ep = APIRouter(prefix="/ping", tags=["pings"])
    __uc: usecases.Ping

    def __init__(self, usecase: usecases.Ping):
        Pings.__uc = usecase

    @staticmethod
    @ep.api_route("", methods=["GET", "HEAD", "OPTIONS"])
    async def ping_server(request: Request):
        with RestContext(request) as ctx:
            return Pings.__uc.server_alive(ctx)

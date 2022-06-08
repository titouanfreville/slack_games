from typing import Any
from uuid import uuid4

from fastapi import Request


class Context(dict):
    """Manage context for BetOnYou API"""

    class Keys:
        REQUEST_ID = "request_id"
        PLAYER = "player"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __duplicates__(self) -> "Context":
        ctx = Context(**self)
        return ctx

    def with_values(self, key: str, value: Any) -> "Context":
        """Add value to new context. Source context is not modified"""
        ctx = self.__duplicates__()
        ctx[key] = value

        return ctx

    def get(self, key, default=None) -> Any:
        """Get value from current context"""
        return super().get(key, default)

    @staticmethod
    def new_from_request(request: Request) -> "Context":
        ctx = Context()

        if hasattr(request.state, "request_id"):
            ctx = ctx.with_values(Context.Keys.REQUEST_ID, request.state.request_id)
        if hasattr(request.state, "user"):
            ctx = ctx.with_values(
                Context.Keys.PLAYER,
                {
                    "id": request.state.user.get("user_id"),
                    "nickname": request.state.user.get("name"),
                    "kind": request.state.user.get("user_kind"),
                },
            )

        return ctx

    @staticmethod
    def new_auto_context() -> "Context":
        return (
            Context()
            .with_values(Context.Keys.REQUEST_ID, uuid4().__str__())
            .with_values(
                Context.Keys.PLAYER,
                {
                    "id": "SYSTEM",
                    "nickname": "SYSTEM",
                },
            )
        )


class RestContext(Context):
    def __init__(self, request: Request):
        self.__request = request

    def __enter__(self):
        ctx = Context()

        if hasattr(self.__request.state, "request_id"):
            ctx = ctx.with_values(Context.Keys.REQUEST_ID, self.__request.state.request_id)
        if hasattr(self.__request.state, "user"):
            ctx = ctx.with_values(
                Context.Keys.PLAYER,
                {
                    "id": self.__request.state.user.get("user_id"),
                    "nickname": self.__request.state.user.get("name"),
                    "kind": self.__request.state.user.get("user_kind"),
                },
            )

        return ctx

    def __exit__(self, type, value, traceback):
        self.__request = None

from http import HTTPStatus
from sys import getsizeof
from time import time_ns
from uuid import uuid4

from asyncstdlib import itertools
from dependency_injector.wiring import Provide
from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception, push_scope
from starlette.responses import StreamingResponse

from app import router
from app.dependencies import SlackGames
from app.domain.errors import BaseException, Details, ErrInvalidData, ErrNotFound, ErrUnauthorized


def run(_=Provide[SlackGames.router]):
    # @router.middleware("http")
    # async def sentry_exception(request: Request, call_next):
    #     def __init_scope(scope, level: str = "error"):
    #         scope.set_context("request", request)  # type:ignore

    #         user_id = (
    #             request.state.user.get("user_id")
    #             if hasattr(request, "state") and hasattr(request.state, "user")
    #             else "not identified"
    #         )

    #         scope.set_level(level)
    #         scope.user = {"ip_address": request.client.host, "id": user_id}

    #     try:
    #         return await call_next(request)

    #     except (ErrUnauthorized, ErrNotFound, ErrInvalidData) as e:
    #         with push_scope() as scope:
    #             __init_scope(scope, "info")
    #             capture_exception(e)

    #             raise e

    #     except Exception as e:
    #         with push_scope() as scope:
    #             __init_scope(scope)
    #             capture_exception(e)

    #             raise e

    # Should always be the latests middleware
    @router.middleware("http")
    async def request(req: Request, call_next):
        async def __exec(__req: Request) -> StreamingResponse | JSONResponse:
            try:
                return await call_next(__req)
            except BaseException as e:
                return JSONResponse(
                    status_code=e.status,
                    content=jsonable_encoder(e.to_json()),
                )
            except RequestValidationError as e:
                raise e
            except ValueError as e:
                # __log_error.error("Unexpected value error when processing request", e)
                valErr = ErrInvalidData("unknown", f"{e}")
                return JSONResponse(
                    status_code=valErr.status,
                    content=jsonable_encoder(valErr.to_json()),
                )
            except HTTPException as e:
                # __log_error.error("Unexpected error when processing request", e)
                return JSONResponse(status_code=e.status_code, content={"ERROR": e.detail})
            except Exception as e:
                # __log_error.error("Unexpected error when processing request", e)
                return JSONResponse(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    content=jsonable_encoder("Internal error"),
                )

        # __log = Log.named("api.log")
        # __log_error = Log.named("core.middleware")
        request_id = req.headers.get("X-Request-ID", uuid4().__str__())

        # __log = __log.parameter("request_id", request_id)
        # __log_error = __log_error.parameter("request_id", request_id)

        req.state.request_id = request_id

        start = time_ns()

        response = await __exec(req)

        response.headers.append("X-Request-ID", request_id)
        end = time_ns()

        # Compute REQUEST LOGS
        # if hasattr(req.state, "user"):
        #     __log = __log.parameter("user_id", req.state.user.get("user_id"))
        #     __log = __log.parameter("nickname", req.state.user.get("name"))

        # Compute data to log
        log_request = {
            "headers": {header: req.headers.get(header) for header in req.headers},
            "url": req.url.__str__(),
            "method": req.method,
            "status": response.status_code,
            "latency": f"{(end - start)/1_000_000_000:.9f}s",
        }

        # COMPUTE RESPONSE LOG
        body = ""
        if hasattr(response, "body_iterator"):
            body_data = itertools.tee(response.body_iterator, 2)  # type: ignore
            body = "\n".join([chunk.decode("utf-8") async for chunk in body_data[0] if chunk])
            response.body_iterator = body_data[1]  # type: ignore
        elif hasattr(response, "body"):
            body = response.body.decode("utf-8")

        MAX_BODY_BYTES_SIZE = 250_000

        # Emit log
        # __log.parameter(
        #     "response",
        #     {
        #         "body": body if getsizeof(body) < MAX_BODY_BYTES_SIZE else "OVERWEIGHTED_BODY",
        #         "headers": {header: req.headers.get(header) for header in req.headers},
        #     },
        # ).request(Log.Request(**log_request)).info()

        return response

    @router.exception_handler(RequestValidationError)
    async def convert_default_request_validation_to_bet_invalid_datas(
        _: Request, exc: RequestValidationError
    ):
        details = []
        for detail in exc.errors():
            err_location = detail.get("loc")
            msg = detail.get("msg", "").split(";", 1)
            key = "undefined"
            val = None

            if err_location:
                if err_location[0] == "body" and len(err_location) >= 2:
                    key = err_location[1]  # type: ignore
                    val = exc.body.get(key) if exc.body else None

            expected_values = None
            if len(msg) > 1:
                expected_values = [
                    val.strip().strip("'")
                    for val in msg[1].strip().removeprefix("permitted:").strip().split(",")
                ]

            details.append(
                Details(
                    key=key,
                    message=msg[0],
                    value={
                        "actual": val,
                        "expected": expected_values,
                    },
                )
            )

        raise ErrInvalidData("body", "bad request data", details)

    return router

from os import path

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.requests import Request

from app import api
from app.core.context import RestContext

basedir = path.dirname(__file__)


serve = api.run()

serve.add_middleware(SentryAsgiMiddleware)

serve.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serve.get("/")
async def home(request: Request):
    with RestContext(request) as ctx:
        print(ctx)

    return {"Hello": "Environment ZAP: {}".format("local")}


if __name__ == "__main__":
    uvicorn.run("test_api:serve", host="0.0.0.0", port=8080, reload=True)  # nosec

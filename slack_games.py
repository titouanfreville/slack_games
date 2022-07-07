import logging
from datetime import datetime
from os import path

import pytz
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import api, dependencies

basedir = path.dirname(__file__)

# # Prepare dependencies
inject = dependencies.SlackGames()
inject.config.from_ini(path.join(basedir, "config.ini"), required=True)


inject.wire(modules=[dependencies, api])
dependencies.setup_api_backgound()


logging.Logger("main").info("API starting...")

serve = api.run()

# serve.add_middleware(SentryAsgiMiddleware)

serve.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serve.get("/utcnow")
def utc_root():
    now = datetime.utcnow().replace(tzinfo=pytz.utc)

    logging.Logger("fastapi.route").info(f"utcnow : {now}")

    return {"now": now}


if __name__ == "__main__":
    uvicorn.run("slack_games:serve", host="0.0.0.0", port=8000, reload=True)  # nosec

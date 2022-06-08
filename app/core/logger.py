import json
import traceback
from copy import copy, deepcopy
from logging import DEBUG, ERROR, INFO, WARNING, Logger, getLevelName, getLogger
from typing import Any, Dict, Optional

from app.core import Context
from app.domain.errors import BetException
from app.tasks.core import Core as CoreTasks
from pydantic import BaseModel, Field


class Log:
    """Wrap python default logging to provide cleanner logging using JSON format."""

    class Request(BaseModel):
        url: str = Field(alias="requestUrl")
        method: str = Field(default="GET", alias="requestMethod")
        status: int = 0
        headers: Dict[str, str] = {}
        latency: str

        class Config:
            allow_population_by_field_name = True

    def __init__(self, tasks: CoreTasks, config: dict, name: str = ""):
        self.__name: str = name
        self.__log: Logger = getLogger(name)

        self.__tasks = tasks
        self.__conf = {"log": config["log"]}
        self.__gcp_active = "gcp" in config["log"]["log_handler"]
        self.__level = getLevelName(config["log"]["level"])
        self.__is_base = True

        self.__request: Optional[Log.Request] = None
        self.__method: str = ""
        self.__message: str = ""
        self.__parameters: Dict[str, Any] = {}
        self.__with_debug = False

    def named(self, name: str) -> "Log":
        return Log(self.__tasks, self.__conf, name)

    def request(self, request: "Log.Request") -> "Log":
        """Add request data to log"""
        log = self.__duplicate__()
        log.__request = request
        return log

    def context(self, ctx: Context) -> "Log":
        """Add BOY context data to logger."""
        log = self.__duplicate__()
        log.__parameters["request_id"] = ctx.get(Context.Keys.REQUEST_ID)
        log.__parameters["ctx_player"] = ctx.get(Context.Keys.PLAYER)

        return log

    def exception(self, err: Exception):
        log = self.__duplicate__()

        if isinstance(err, BetException):
            log.parameter("error", err.to_json())
        else:
            log.parameter("error", str(err))

        return log

    def method(self, method: str) -> "Log":
        """Add current logged method name to logger."""
        log = self.__duplicate__()
        log.__method = f"[{method}] "
        return log

    def message(self, msg: str) -> "Log":
        """Set logger message"""
        log = self.__duplicate__()
        log.__message = msg
        return log

    def parameter(self, key: str, data: Any) -> "Log":
        """
        Add any value to log under provided key.
        /!\\ erase key if already defined.
        """
        log = self.__duplicate__()
        log.__parameters[key] = data if not hasattr(data, "to_log") else data.to_log()
        return log

    def with_debug(self) -> "Log":
        """Add debug stack information to log."""
        log = self.__duplicate__()
        log.__with_debug = True
        return log

    def success(self, msg: str = None):
        """Emit success log with optional message."""
        self.info("Success!" + (" " + msg if msg else ""))

    def info(self, msg: str = None):
        """Emit info log. You can provide a message witch will be placed before existing message."""
        if self.__level <= INFO:
            if msg:
                self.__message = msg + " " + self.__message

            self.__gcp_log("INFO")
            self.__log.info(self.__msg, stack_info=self.__with_debug, exc_info=self.__with_debug)

        self.__reset()

    def error(self, msg: str = None, error: Exception = None):
        """
        Emit error log. You can provide a message witch will be placed
        before existing message and a exception to log under `error` key.
        /!\\ Debug trace is always included on error.
        """
        if self.__level <= ERROR:
            if msg:
                self.__message = msg + " " + self.__message

            if error:
                self.parameter("error", str(error))

            self.__with_debug = True
            self.__log.error(self.__msg, stack_info=True, exc_info=True)
            self.__gcp_log("ERROR")

        self.__reset()

    def warning(self, msg: str = None, error: Exception = None):
        """
        Emit warning log. You can provide a message witch will be placed
        before existing message and a exception to log under `error` key.
        """
        if self.__level <= WARNING:
            if msg:
                self.__message = msg + " " + self.__message
            if error:
                self.parameter("error", str(error))

            self.__gcp_log("WARNING")
            self.__log.warning(
                self.__msg, stack_info=self.__with_debug, exc_info=self.__with_debug
            )

        self.__reset()

    def debug(self, msg: str = None):
        """
        Emit debug log. You can provide a message witch will be placed before existing message.
        """
        if self.__level <= DEBUG:
            if msg:
                self.__message = msg + " " + self.__message

            self.__gcp_log("DEBUG")
            self.__log.debug(self.__msg, stack_info=self.__with_debug, exc_info=self.__with_debug)

        self.__reset()

    def _duplicate(self) -> "Log":
        log = Log(self.__tasks, self.__conf)
        log.__is_base = False

        log.__name = self.__name
        log.__log = self.__log

        log.__parameters = deepcopy(self.__parameters)
        log.__request = self.__request
        log.__method = self.__method
        log.__message = self.__message
        log.__with_debug = copy(self.__with_debug)

        return log

    @property
    def __msg(self) -> str:
        data = self.__json_data
        if self.__request:
            data["request"] = self.__request.dict()

        return json.dumps(data, sort_keys=True)

    @property
    def __json_data(self) -> dict:
        data = self.__parameters
        if self.__method or self.__message:
            data["message"] = f"{self.__method}{self.__message}"

        return data

    def __duplicate__(self) -> "Log":
        if not self.__is_base:
            return self

        log = Log(self.__tasks, self.__conf, self.__name)
        log.__is_base = False

        return log

    def __reset(self):
        self.__method: str = ""
        self.__message: str = ""
        self.__parameters: Any = {}
        self.__with_debug = False

    def __gcp_log(self, severity: str = "INFO"):
        if self.__gcp_active:
            data = self.__json_data
            if self.__with_debug:
                data["trace"] = traceback.format_exc(100)
                data["stack"] = traceback.format_stack(limit=100)

            if not self.__request:
                self.__tasks.gcp_log.send(self.__name, data, severity)
            else:
                self.parameter("request", self.__request.dict())
                self.__tasks.gcp_log.send(
                    self.__name,
                    data,
                    severity,
                    self.__request.dict(exclude={"body", "headers"}, by_alias=True),
                )

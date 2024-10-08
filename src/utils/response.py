from enum import Enum
from typing import Any, Literal
from pydantic import model_validator, model_serializer

from utils.schemas import BaseModel


class ErrorCodes(Enum):
    """
    Enum of response error codes.
    For description see documentation
    """

    INTERNAL_SERVER_ERROR = 1
    UNPROCESSABLE_ENTITY = 2
    TOKEN_EXPIRED = 3
    TOKEN_VALIDATION_FAILED = 4
    NOT_FOUND = 5
    ACCESS_DENIED = 6
    DOMAIN_ALREADY_TAKEN = 7
    EMAIL_ALREADY_TAKEN = 8
    USER_ALREADY_MEMBER = 9


class ErrorResponse(Exception):
    """Response with custom error code"""

    code: ErrorCodes
    message: str | None
    http_status_code: int
    auto_message: bool
    """If main message is None, it makes message be error code representation"""

    def __init__(
        self, code: ErrorCodes, message: str | None = None, http_status_code: int = 400, auto_message: bool = False
    ):
        self.code = code
        self.message = message
        self.http_status_code = http_status_code
        self.auto_message = auto_message


class SuccessfulResponse[T: BaseModel | None](BaseModel):
    @model_validator(mode="before")
    @classmethod
    def before_validation(cls, data) -> dict[str, Any]:
        return {"proxy": data}

    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        if self.proxy is None:
            return {"ok": self.ok}
        return {"ok": self.ok, **self.proxy.model_dump()}

    ok: Literal[True] = True
    proxy: T

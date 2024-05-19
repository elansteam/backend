"""Some useful stuff"""

from enum import Enum


class ResponseErrorCodes(Enum):
    """
    Enum of response error codes.
    For description see documentation TODO: set documentation url
    """
    INTERNAL_SERVER_ERROR = 1
    UNPROCESSABLE_ENTITY = 2
    TOKEN_EXPIRED = 3
    TOKEN_VALIDATION_FAILED = 4
    COULD_NOT_FIND_USER_BY_TOKEN = 5
    INCORRECT_AUTH_HEADER_FOMAT = 6
    ACCESS_DENIED = 7

class ResponseWithErrorCode(Exception):
    """Response with custom error code"""

    code: ResponseErrorCodes
    message: str | None
    http_status_code: int
    auto_message: bool  # experemental
    """If main message is None, it makes message be error code representation"""

    def __init__(
        self,
        code: ResponseErrorCodes,
        message: str | None = None,
        http_status_code: int = 400,
        auto_message: bool = False
    ):
        self.code = code
        self.message = message
        self.http_status_code = http_status_code
        self.auto_message = auto_message

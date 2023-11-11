from typing import List

from starlette.responses import JSONResponse


def get_error_schema(description: str, msg: str = "error msg"):
    return {"description": description,
            "content": {
                "application/json": {
                    "example": {"detail": [{
                        "msg": msg,
                    }]},
                }
            }}


def get_error_response(msg: str, status_code: int = 400):
    """Сообщение об ошибке"""
    return JSONResponse(status_code=status_code, content={"detail": [
        {"msg": msg}
    ]})


def has_role_permission(role: List[str], permission: str):
    return permission in role

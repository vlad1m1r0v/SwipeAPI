from typing import Callable, Any

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from src.users.exceptions import UserAlreadyExistsException


def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def setup_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with given email already exists",
                "error_code": "user_exists",
            },
        ),
    )

__all__ = "setup_error_handlers"

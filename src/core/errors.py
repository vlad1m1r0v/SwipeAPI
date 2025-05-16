from typing import Callable, Any

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from jwt import InvalidTokenError
from src.auth.exceptions import (
    InvalidTokenTypeException,
    UnauthorizedException
)

from src.users.exceptions import (
    UserAlreadyExistsException,
    UserDoesNotExistException,
    IncorrectPasswordException,
    InvalidRoleException
)


def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UnauthorizedException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Unauthorized request",
                "error_code": "unauthorized_request",
            },
        )
    )

    app.add_exception_handler(
        InvalidTokenError,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid token",
                "error_code": "invalid_token",
            },
        )
    )

    app.add_exception_handler(
        InvalidTokenTypeException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid token type",
                "error_code": "invalid_token_type",
            },
        ),
    )

    app.add_exception_handler(
        UserAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with given email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserDoesNotExistException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User with given email does not exist",
                "error_code": "user_does_not_exist",
            },
        ),
    )

    app.add_exception_handler(
        IncorrectPasswordException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Password is incorrect",
                "error_code": "incorrect_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidRoleException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have permission to perform this action",
                "error_code": "invalid_role",
            },
        ),
    )

    __all__ = "setup_exception_handlers"

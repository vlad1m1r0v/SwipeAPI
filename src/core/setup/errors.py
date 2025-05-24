from typing import Callable, Any

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from advanced_alchemy.exceptions import (
    IntegrityError,
    DuplicateKeyError,
    NotFoundError
)

from jwt import InvalidTokenError

from src.auth.exceptions import (
    TokenNotProvidedException,
    InvalidTokenTypeException,
    UnauthorizedException
)

from src.users.exceptions import (
    UserAlreadyExistsException,
    IncorrectPasswordException,
    InvalidRoleException,
    BalanceNotFoundException,
    UserDoesNotExistException,
    SubscriptionExpiredException,
    UserBlacklistedException
)


def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def setup_exception_handlers(app: FastAPI) -> None:
    # region database
    app.add_exception_handler(
        IntegrityError,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": "Unable to complete request because of integrity error."},
        )
    )

    app.add_exception_handler(
        DuplicateKeyError,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": " A record matching the supplied data already exists."},
        )
    )

    app.add_exception_handler(
        NotFoundError,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": " The requested resource was not found."},
        )
    )
    # endregion database

    # region auth
    app.add_exception_handler(
        UnauthorizedException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Unauthorized request."},
        )
    )

    app.add_exception_handler(
        TokenNotProvidedException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Token was not provided."},
        )
    )

    app.add_exception_handler(
        InvalidTokenError,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Invalid token."},
        )
    )

    app.add_exception_handler(
        InvalidTokenTypeException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Invalid token type."},
        ),
    )

    app.add_exception_handler(
        IncorrectPasswordException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Password is incorrect."},
        ),
    )

    app.add_exception_handler(
        InvalidRoleException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={"message": "You do not have permission to perform this action."},
        ),
    )
    # endregion auth

    # region users
    app.add_exception_handler(
        UserAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with given email already exists."},
        ),
    )

    app.add_exception_handler(
        UserDoesNotExistException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "User with given email does not exist."},
        ),
    )

    app.add_exception_handler(
        BalanceNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Balance was not found."},
        ),
    )

    app.add_exception_handler(
        SubscriptionExpiredException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Subscription is expired."},
        ),
    )

    app.add_exception_handler(
        UserBlacklistedException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "User is blacklisted by moderation."},
        ),
    )
    # endregion users

    __all__ = "setup_exception_handlers"

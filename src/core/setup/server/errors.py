from typing import Callable, Any

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from advanced_alchemy.exceptions import IntegrityError, DuplicateKeyError, NotFoundError

from src.core.exceptions import (
    IntegrityErrorException,
    DuplicateKeyException,
    NotFoundException,
)
from src.core.utils import DefaultHTTPException


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def default_http_exception_handler(request: Request, exc: DefaultHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": {
                "code": exc.error,
                "details": {
                    "field": exc.field,
                    "message": exc.message,
                },
            },
        },
    )


async def database_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, IntegrityError):
        raise IntegrityErrorException()
    elif isinstance(exc, DuplicateKeyError):
        raise DuplicateKeyException()
    elif isinstance(exc, NotFoundError):
        raise NotFoundException()


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(DuplicateKeyError, database_exception_handler)
    app.add_exception_handler(NotFoundError, database_exception_handler)

    app.add_exception_handler(DefaultHTTPException, default_http_exception_handler)


__all__ = ["setup_exception_handlers"]

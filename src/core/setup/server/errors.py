from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from starlette import status
from starlette.responses import JSONResponse

from advanced_alchemy.exceptions import IntegrityError, DuplicateKeyError, NotFoundError

from src.core.exceptions import (
    IntegrityErrorException,
    DuplicateKeyException,
    NotFoundException,
)
from src.core.exceptions.base import DefaultHTTPException


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


def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        location = ".".join(str(loc) for loc in err.get("loc", []))
        field = err.get("loc", [None])[-1]
        errors.append(
            {
                "location": location,
                "field": field,
                "message": err.get("msg", "Invalid input"),
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": 422,
            "error": {
                "code": "VALIDATION_ERROR",
                "details": errors,
            },
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(DuplicateKeyError, database_exception_handler)
    app.add_exception_handler(NotFoundError, database_exception_handler)

    app.add_exception_handler(DefaultHTTPException, default_http_exception_handler)

    app.add_exception_handler(RequestValidationError, validation_error_handler)


__all__ = ["setup_exception_handlers"]

from starlette import status

from src.core.exceptions.base import DefaultHTTPException


class IsNotOwnerException(DefaultHTTPException):
    error = "NOT_OWNER"
    message = "You are not the owner of this resource."
    field = "owner"
    status_code = status.HTTP_403_FORBIDDEN


class IntegrityErrorException(DefaultHTTPException):
    error = "INTEGRITY_ERROR"
    message = "Integrity error occurred."
    field = "database"
    status_code = status.HTTP_409_CONFLICT


class DuplicateKeyException(DefaultHTTPException):
    error = "DUPLICATE_KEY"
    message = "Duplicate record exists."
    field = "database"
    status_code = status.HTTP_409_CONFLICT


class NotFoundException(DefaultHTTPException):
    error = "NOT_FOUND"
    message = "Requested resource not found."
    field = "database"
    status_code = status.HTTP_404_NOT_FOUND

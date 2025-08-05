from starlette import status

from src.core.exceptions.base import DefaultHTTPException


class FiltersAmountExceededException(DefaultHTTPException):
    error = "FILTERS_AMOUNT_EXCEEDED"
    message = "FILTERS_AMOUNT_EXCEEDED."
    field = "filter"
    status_code = status.HTTP_403_FORBIDDEN

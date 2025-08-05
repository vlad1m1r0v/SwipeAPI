from starlette import status

from src.core.exceptions.base import DefaultHTTPException


class FiltersAmountExceededException(DefaultHTTPException):
    error = "FILTERS_AMOUNT_EXCEEDED"
    message = "Filter amount exceeded."
    field = "filter"
    status_code = status.HTTP_403_FORBIDDEN

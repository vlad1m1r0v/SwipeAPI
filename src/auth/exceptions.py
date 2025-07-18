from starlette import status
from src.core.exceptions.base import DefaultHTTPException


class TokenNotProvidedException(DefaultHTTPException):
    error = "TOKEN_NOT_PROVIDED"
    message = "Token was not provided."
    field = "token"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenTypeException(DefaultHTTPException):
    error = "INVALID_TOKEN_TYPE"
    message = "Invalid token type."
    field = "token"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenAlreadyUsedException(DefaultHTTPException):
    error = "TOKEN_ALREADY_USED"
    message = "Token has already been used."
    field = "token"
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedException(DefaultHTTPException):
    error = "UNAUTHORIZED"
    message = "Authorization credentials were not provided."
    field = "authorization"
    status_code = status.HTTP_401_UNAUTHORIZED


class SignatureExpiredException(DefaultHTTPException):
    error = "SIGNATURE_EXPIRED"
    message = "Token signature has expired."
    field = "token"
    status_code = status.HTTP_400_BAD_REQUEST


class BadSignatureException(DefaultHTTPException):
    error = "BAD_SIGNATURE"
    message = "Invalid token signature."
    field = "token"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidTokenException(DefaultHTTPException):
    error = "INVALID_TOKEN"
    message = "Provided token is invalid."
    field = "token"
    status_code = status.HTTP_400_BAD_REQUEST

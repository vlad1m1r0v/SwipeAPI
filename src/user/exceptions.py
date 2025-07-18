from starlette import status
from src.core.exceptions.base import DefaultHTTPException


class UserAlreadyExistsException(DefaultHTTPException):
    error = "USER_ALREADY_EXISTS"
    message = "User already exists."
    field = "email"
    status_code = status.HTTP_400_BAD_REQUEST


class UserDoesNotExistException(DefaultHTTPException):
    error = "USER_DOES_NOT_EXIST"
    message = "User with provided credentials does not exist."
    field = "email"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectPasswordException(DefaultHTTPException):
    error = "INCORRECT_PASSWORD"
    message = "Incorrect password."
    field = "password"
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidRoleException(DefaultHTTPException):
    error = "INVALID_ROLE"
    message = "Invalid role for this resource."
    field = "role"
    status_code = status.HTTP_403_FORBIDDEN


class SubscriptionExpiredException(DefaultHTTPException):
    error = "SUBSCRIPTION_EXPIRED"
    message = "Subscription has expired."
    field = "subscription"
    status_code = status.HTTP_403_FORBIDDEN


class NotEnoughMoneyException(DefaultHTTPException):
    error = "NOT_ENOUGH_MONEY"
    message = "Not enough balance."
    field = "balance"
    status_code = status.HTTP_402_PAYMENT_REQUIRED


class UserBlacklistedException(DefaultHTTPException):
    error = "USER_BLACKLISTED"
    message = "User is blacklisted."
    field = "user"
    status_code = status.HTTP_403_FORBIDDEN

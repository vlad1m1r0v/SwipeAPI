class UserAlreadyExistsException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass


class IncorrectPasswordException(Exception):
    pass


class InvalidRoleException(Exception):
    pass


class SubscriptionExpiredException(Exception):
    pass


class UserBlacklistedException(Exception):
    pass

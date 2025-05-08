import enum


class UserRoleEnum(str, enum.Enum):
    BUILDER = "Builder"
    USER = "User"
    ADMIN = "Admin"


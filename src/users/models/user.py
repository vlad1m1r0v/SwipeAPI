import enum
from sqlalchemy import Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class UserRoleEnum(str, enum.Enum):
    BUILDER = "Builder"
    USER = "User"
    ADMIN = "Admin"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    photo: Mapped[str | None]
    email: Mapped[str]
    phone: Mapped[str]
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role_enum"),
        nullable=False,
        default=UserRoleEnum.USER
    )
    password: Mapped[str]

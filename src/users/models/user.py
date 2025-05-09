from typing import TYPE_CHECKING

from sqlalchemy import Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.users.enums import UserRoleEnum

if TYPE_CHECKING:
    from .contact import ContactModel
    from .agent_contact import AgentContactModel
    from .subscription import SubscriptionModel
    from .notification_settings import NotificationSettingsModel
    from .balance import BalanceModel



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

    contact: Mapped["ContactModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    agent_contact: Mapped["AgentContactModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    subscription: Mapped["SubscriptionModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    notification_settings: Mapped["NotificationSettingsModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    balance: Mapped["BalanceModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

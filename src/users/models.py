import typing
from datetime import datetime, UTC, timedelta
from decimal import Decimal

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase, orm_registry
from advanced_alchemy.types import FileObject, StoredObject

import src.users.enums as enums
import src.users.constants as constants

METADATA: typing.Final = orm_registry.metadata
orm.DeclarativeBase.metadata = METADATA


class Contact(BigIntAuditBase):
    __tablename__ = "contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str]
    email: orm.Mapped[str]

    user: orm.Mapped['User'] = orm.relationship(back_populates="contact")


class AgentContact(BigIntAuditBase):
    __tablename__ = "agent_contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str | None]
    email: orm.Mapped[str | None]

    user: orm.Mapped["User"] = orm.relationship(back_populates="agent_contact")


class Subscription(BigIntAuditBase):
    __tablename__ = "subscriptions"

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    is_auto_renewal: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    expiry_date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime,
                                                          default=lambda: datetime.now(UTC).replace(
                                                              tzinfo=None) + timedelta(days=30))

    user: orm.Mapped["User"] = orm.relationship(back_populates="subscription")


class NotificationSettings(BigIntAuditBase):
    __tablename__ = "notification_settings"

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    redirect_notifications_to_agent: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    notification_type: orm.Mapped[enums.NotificationTypeEnum] = orm.mapped_column(
        sa.Enum(enums.NotificationTypeEnum, name="notification_type_enum"),
        nullable=False,
        default=enums.NotificationTypeEnum.DISABLED,
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="notification_settings")


class Balance(BigIntAuditBase):
    __tablename__ = "balances"

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    value: orm.Mapped[Decimal] = orm.mapped_column(sa.Numeric(precision=12, scale=2), default=constants.DEFAULT_BALANCE,
                                                   server_default=str(constants.DEFAULT_BALANCE))

    user: orm.Mapped["User"] = orm.relationship(back_populates="balance")


class User(BigIntAuditBase):
    __tablename__ = "users"

    name: orm.Mapped[str]
    photo: orm.Mapped[FileObject | None] = orm.mapped_column(StoredObject(backend="local"))
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
    role: orm.Mapped[enums.UserRoleEnum] = orm.mapped_column(
        sa.Enum(enums.UserRoleEnum, name="user_role_enum"),
        nullable=False,
        default=enums.UserRoleEnum.USER
    )
    password: orm.Mapped[str]

    contact: orm.Mapped["Contact"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    agent_contact: orm.Mapped["AgentContact"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    subscription: orm.Mapped["Subscription"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    notification_settings: orm.Mapped["NotificationSettings"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    balance: orm.Mapped["Balance"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


__all__ = [
    'METADATA',
    'Contact',
    'AgentContact',
    'Subscription',
    'NotificationSettings',
    'Balance',
    'User'
]

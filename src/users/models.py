from typing import TYPE_CHECKING
from datetime import datetime, UTC, timedelta
from decimal import Decimal


from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from sqlalchemy_file import FileField

from src.core.enums import STORAGE_CONTAINER

import src.users.enums as enums
import src.users.constants as constants

if TYPE_CHECKING:
    from src.admins.models import Blacklist


class Contact(BigIntAuditBase):
    __tablename__ = "contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str]
    email: orm.Mapped[str]

    user: orm.Mapped['User'] = orm.relationship(back_populates="contact")


class AgentContact(BigIntAuditBase):
    __tablename__ = "agent_contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str | None]
    email: orm.Mapped[str | None]

    user: orm.Mapped["User"] = orm.relationship(back_populates="agent_contact")


class Subscription(BigIntAuditBase):
    __tablename__ = "subscriptions"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    is_auto_renewal: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None) + timedelta(days=30)
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="subscription")


class NotificationSettings(BigIntAuditBase):
    __tablename__ = "notification_settings"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    redirect_notifications_to_agent: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    notification_type: orm.Mapped[enums.NOTIFICATION_TYPE] = orm.mapped_column(
        sa.Enum(enums.NOTIFICATION_TYPE, name="notification_type_enum"),
        nullable=False,
        default=enums.NOTIFICATION_TYPE.DISABLED,
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="notification_settings")


class Balance(BigIntAuditBase):
    __tablename__ = "balances"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    value: orm.Mapped[Decimal] = orm.mapped_column(
        sa.Numeric(precision=12, scale=2),
        default=constants.DEFAULT_BALANCE
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="balance")


class User(BigIntAuditBase):
    __tablename__ = "users"

    name: orm.Mapped[str]
    photo = sa.Column(
        FileField(
            upload_storage=STORAGE_CONTAINER.IMAGES,
        )
    )
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
    role: orm.Mapped[enums.ROLE] = orm.mapped_column(
        sa.Enum(enums.ROLE, name="user_role_enum"),
        nullable=False,
        default=enums.ROLE.USER
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
    blacklist: orm.Mapped["Blacklist"] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


__all__ = [
    'User',
    'Contact',
    'AgentContact',
    'Subscription',
    'NotificationSettings',
    'Balance'
]

from typing import TYPE_CHECKING

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import JSONB
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.users.enums import Role

if TYPE_CHECKING:
    from src.users.models import (
        Contact,
        AgentContact,
        Subscription,
        NotificationSettings,
        Balance
    )

    from src.admins.models import Blacklist


class User(BigIntAuditBase):
    __tablename__ = "users"

    name: orm.Mapped[str]
    photo = sa.Column(JSONB)
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
    role: orm.Mapped[Role] = orm.mapped_column(
        sa.Enum(Role, name="user_role_enum"),
        nullable=False,
        default=Role.USER
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

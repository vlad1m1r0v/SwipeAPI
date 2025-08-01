from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.user.enums import Role

if TYPE_CHECKING:
    from src.user.models import (
        Contact,
        AgentContact,
        Subscription,
        NotificationSettings,
        Balance,
    )

    from src.admin.models import Blacklist

    from src.builder.models import Complex, FavouriteComplex

    from src.apartments.models import Apartment

    from src.announcements.models import (
        AnnouncementView,
        FavouriteAnnouncement,
        Filter,
        Complaint,
    )


class User(BigIntAuditBase):
    __tablename__ = "users"

    name: orm.Mapped[str]
    photo: orm.Mapped[Optional[str]] = orm.mapped_column(nullable=True)
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
    role: orm.Mapped[Role] = orm.mapped_column(
        sa.Enum(Role, name="user_role_enum"), nullable=False, default=Role.USER
    )
    password: orm.Mapped[str]
    contact: orm.Mapped["Contact"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    agent_contact: orm.Mapped["AgentContact"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    subscription: orm.Mapped["Subscription"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    notification_settings: orm.Mapped["NotificationSettings"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    balance: orm.Mapped["Balance"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    blacklist: orm.Mapped["Blacklist"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    complex: orm.Mapped["Complex"] = orm.relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    apartments: orm.Mapped[List["Apartment"]] = orm.relationship(
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )
    views: orm.Mapped[List["AnnouncementView"]] = orm.relationship(
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )
    favourite_announcements: orm.Mapped[List["FavouriteAnnouncement"]] = (
        orm.relationship(
            back_populates="user",
            uselist=True,
            cascade="all, delete-orphan",
        )
    )
    filters: orm.Mapped[List["Filter"]] = orm.relationship(
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )
    complaints: orm.Mapped[List["Complaint"]] = orm.relationship(
        uselist=True,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    favourite_complexes: orm.Mapped[List["FavouriteComplex"]] = orm.relationship(
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

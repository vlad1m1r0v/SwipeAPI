from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.builder.enums import Technology, PropertyType, Heating

from src.apartments.enums import (
    OwnershipType,
    Bedrooms,
    Bathrooms,
    Commission,
    ApartmentCondition,
    Finishing,
    Rooms,
    CallMethod,
)

from src.requests.models import AddToComplexRequest

if TYPE_CHECKING:
    from src.user.models import User

    from src.buildings.models import Riser, Floor

    from src.announcements.models import Announcement

    from src.apartments.models import ApartmentGallery


class Apartment(BigIntAuditBase):
    __tablename__ = "apartments"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    floor_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.ForeignKey("floors.id", ondelete="SET NULL"), nullable=True
    )
    riser_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.ForeignKey("risers.id", ondelete="SET NULL"), nullable=True
    )
    address: orm.Mapped[str]
    district: orm.Mapped[str]
    microdistrict: orm.Mapped[str]
    longitude: orm.Mapped[Decimal] = orm.mapped_column(sa.Numeric(precision=6, scale=3))
    latitude: orm.Mapped[Decimal] = orm.mapped_column(sa.Numeric(precision=6, scale=3))
    technology: orm.Mapped[Technology] = orm.mapped_column(
        sa.Enum(Technology, name="apartment_technology_enum")
    )
    ownership_type: orm.Mapped[OwnershipType] = orm.mapped_column(
        sa.Enum(OwnershipType, name="apartment_ownership_type_enum")
    )
    property_type: orm.Mapped[PropertyType] = orm.mapped_column(
        sa.Enum(PropertyType, name="apartment_property_type_enum")
    )
    bedrooms: orm.Mapped[Bedrooms] = orm.mapped_column(
        sa.Enum(Bedrooms, name="apartment_bedrooms_enum")
    )
    bathrooms: orm.Mapped[Bathrooms] = orm.mapped_column(
        sa.Enum(Bathrooms, name="apartment_bathrooms_enum")
    )
    kitchen_area: orm.Mapped[Decimal] = orm.mapped_column(
        sa.Numeric(precision=3, scale=1)
    )
    heating: orm.Mapped[Heating] = orm.mapped_column(
        sa.Enum(Heating, name="apartment_heating_enum")
    )
    has_balcony_or_loggia: orm.Mapped[bool] = orm.mapped_column(sa.Boolean)
    has_mortgage: orm.Mapped[bool] = orm.mapped_column(sa.Boolean)
    commission_to_agent: orm.Mapped[Commission] = orm.mapped_column(
        sa.Enum(Commission, name="apartment_commission_enum")
    )
    condition: orm.Mapped[ApartmentCondition] = orm.mapped_column(
        sa.Enum(ApartmentCondition, name="apartment_condition_enum")
    )
    finishing: orm.Mapped[Finishing] = orm.mapped_column(
        sa.Enum(Finishing, name="apartment_finishing_enum")
    )
    rooms: orm.Mapped[Rooms] = orm.mapped_column(
        sa.Enum(Rooms, name="apartment_rooms_enum")
    )
    area: orm.Mapped[Decimal] = orm.mapped_column(sa.Numeric(precision=5, scale=1))
    call_method: orm.Mapped[CallMethod] = orm.mapped_column(
        sa.Enum(CallMethod, name="apartment_call_method_enum")
    )
    description: orm.Mapped[str | None] = sa.Column(sa.Text)
    price: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    scheme: orm.Mapped[str]

    user: orm.Mapped["User"] = orm.relationship(back_populates="apartments")
    floor: orm.Mapped["Floor"] = orm.relationship(back_populates="apartments")
    riser: orm.Mapped["Riser"] = orm.relationship(back_populates="apartments")
    gallery: orm.Mapped[List["ApartmentGallery"]] = orm.relationship(
        back_populates="apartment",
        uselist=True,
        cascade="all, delete-orphan",
        order_by="ApartmentGallery.order",
    )
    requests: orm.Mapped[List["AddToComplexRequest"]] = orm.relationship(
        "AddToComplexRequest",
        uselist=True,
        back_populates="apartment",
        cascade="all, delete-orphan",
    )
    announcement: orm.Mapped["Announcement"] = orm.relationship(
        back_populates="apartment"
    )

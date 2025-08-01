from datetime import datetime
from decimal import Decimal

from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.core.constants import PHONE_NUMBER

from src.auth.schemas import PasswordMixin

from src.user.enums import Role, NotificationType

from src.builder.schemas import (
    CreateDocumentSchema as _CreateDocumentSchema,
    CreateNewsSchema as _CreateNewsSchema,
)
from src.builder.enums import (
    Status,
    Type,
    Class,
    Technology,
    Territory,
    UtilityBills,
    Heating,
    Sewerage,
    WaterSupply,
    Formalization,
    BillingOptions,
    PropertyType,
    SumInContract,
)

from src.apartments.schemas import CreateApartmentSchema as _CreateApartmentSchema

from src.announcements.schemas import (
    CreateFavouriteAnnouncementSchema as _CreateFavouriteAnnouncementSchema,
    CreateFilterSchema as _CreateFilterSchema,
)


class CreateUserSchema(PasswordMixin):
    name: str = Field(min_length=3, max_length=100)
    phone: str = Field(pattern=PHONE_NUMBER)
    email: EmailStr
    photo: Optional[str] = None
    role: Optional[Role] = Field(default=Role.USER)


class CreateContactSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone: str
    email: str


class CreateAgentContactSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr


class CreateSubscriptionSchema(BaseModel):
    user_id: int
    is_auto_renewal: bool
    expiry_date: datetime


class CreateNotificationSettingsSchema(BaseModel):
    user_id: int
    redirect_notifications_to_agent: bool
    notification_type: NotificationType


class CreateBalanceSchema(BaseModel):
    user_id: int
    value: float


class CreateComplexSchema(BaseModel):
    user_id: int
    name: str
    address: str
    description: str
    longitude: Decimal
    latitude: Decimal


class CreateInfrastructureSchema(BaseModel):
    complex_id: int
    status: Status
    type: Type
    infrastructure_class: Class
    technology: Technology
    territory: Territory
    sea_distance: Decimal
    utility_bills: UtilityBills
    ceiling_height: Decimal
    has_gas: bool
    heating: Heating
    sewerage: Sewerage
    water_supply: WaterSupply


class CreateAdvantagesSchema(BaseModel):
    complex_id: int
    has_children_playground: bool
    has_sports_field: bool
    has_parking: bool
    has_landscaped_area: bool
    has_on_site_shops: bool
    has_individual_heating: bool
    has_balcony_or_loggia: bool
    has_bicycle_field: bool
    has_panoramic_windows: bool
    is_close_to_sea: bool
    is_close_to_school: bool
    is_close_to_transport: bool


class CreateFormalizationAndPaymentSettingsSchema(BaseModel):
    complex_id: int
    formalization: Formalization
    billing_options: BillingOptions
    property_type: PropertyType
    sum_in_contract: SumInContract


class CreateBlockSchema(BaseModel):
    complex_id: int
    no: int


class CreateFloorSchema(BaseModel):
    block_id: int
    no: int


class CreateSectionSchema(BaseModel):
    block_id: int
    no: int


class CreateRiserSchema(BaseModel):
    section_id: int
    no: int


class CreateDocumentSchema(_CreateDocumentSchema):
    complex_id: int


class CreateNewsSchema(_CreateNewsSchema):
    complex_id: int


class CreateBuildingImageSchema(BaseModel):
    complex_id: int
    photo: str
    order: int


class CreateApartmentSchema(_CreateApartmentSchema):
    user_id: int
    floor_id: Optional[int] = Field(default=None)
    riser_id: Optional[int] = Field(default=None)


class CreateApartmentImageSchema(BaseModel):
    apartment_id: int
    photo: str
    order: int


class CreateFavouriteAnnouncementSchema(_CreateFavouriteAnnouncementSchema):
    user_id: int


class CreateFilterSchema(_CreateFilterSchema):
    user_id: int


class CreateViewSchema(BaseModel):
    announcement_id: int
    user_id: int

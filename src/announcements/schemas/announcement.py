from typing import Optional

from datetime import time

from pydantic import BaseModel

from src.apartments.schemas import (
    GetApartmentUserListSchema,
    GetApartmentUserDetail as _GetApartmentUserDetail,
)

from src.user.schemas import GetContactSchema

from .promotion import GetPromotionSchema


class CreateAnnouncementSchema(BaseModel):
    apartment_id: int
    viewing_time: time


class UpdateAnnouncementSchema(BaseModel):
    viewing_time: time


class GetAnnouncementUserListSchema(BaseModel):
    id: int
    viewing_time: time
    is_relevant: bool
    is_approved: Optional[bool] = None
    apartment: GetApartmentUserListSchema
    promotion: GetPromotionSchema


class GetApartmentDetailSchema(_GetApartmentUserDetail):
    contact: GetContactSchema


class GetAnnouncementSharedDetailSchema(BaseModel):
    id: int
    viewing_time: time
    is_relevant: bool
    is_approved: Optional[bool] = None
    apartment: GetApartmentDetailSchema
    promotion: GetPromotionSchema


class GetAnnouncementUserDetailSchema(GetAnnouncementSharedDetailSchema):
    views_count: int
    favourites_count: int

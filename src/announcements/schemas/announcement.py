from typing import Optional

from datetime import time

from pydantic import BaseModel

from src.apartments.schemas import GetApartmentUserDetail


class CreateAnnouncementSchema(BaseModel):
    apartment_id: int
    viewing_time: time


class GetAnnouncementUserSchema(BaseModel):
    id: int
    viewing_time: time
    is_relevant: bool
    is_approved: Optional[bool] = None
    apartment: GetApartmentUserDetail


class GetAnnouncementOwnerSchema(GetAnnouncementUserSchema):
    views_count: int
    favorites_count: int

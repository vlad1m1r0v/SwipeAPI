from pydantic import BaseModel

from .announcement import (
    GetAnnouncementUserListSchema,
    GetAnnouncementSharedDetailSchema,
)


class CreateFavouriteAnnouncementSchema(BaseModel):
    announcement_id: int


class GetFavouriteAnnouncementUserListSchema(BaseModel):
    id: int
    announcement: GetAnnouncementUserListSchema


class GetFavouriteAnnouncementUserDetailSchema(BaseModel):
    id: int
    announcement: GetAnnouncementSharedDetailSchema

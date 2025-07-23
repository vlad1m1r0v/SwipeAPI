from pydantic import BaseModel


class CreateFavouriteAnnouncementSchema(BaseModel):
    announcement_id: int
    user_id: int

from typing import Optional

from pydantic import BaseModel


class CreateComplaintSchema(BaseModel):
    announcement_id: int
    is_incorrect_price: Optional[bool] = False
    is_incorrect_photo: Optional[bool] = False
    is_incorrect_description: Optional[bool] = False

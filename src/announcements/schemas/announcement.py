from datetime import time
from pydantic import BaseModel
from typing import Optional


class CreateAnnouncementSchema(BaseModel):
    apartment_id: int
    is_relevant: bool = True
    viewing_time: time
    is_approved: Optional[bool] = None

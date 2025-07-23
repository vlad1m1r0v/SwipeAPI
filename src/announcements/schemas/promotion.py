from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.announcements.enums import Colour, Phrase


class CreatePromotionSchema(BaseModel):
    announcement_id: int
    highlight_colour: Optional[Colour] = None
    highlight_expiry_date: Optional[datetime] = None
    phrase: Optional[Phrase] = None
    phrase_expiry_date: Optional[datetime] = None
    big_advert_expiry_date: Optional[datetime] = None
    boost_expiry_date: Optional[datetime] = None

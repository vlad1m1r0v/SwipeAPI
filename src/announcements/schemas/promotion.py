from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.announcements.enums import Colour, Phrase


class CreatePromotionSchema(BaseModel):
    announcement_id: int
    highlight_colour: Optional[Colour] = None
    highlight_expiry_date: Optional[datetime] = None
    phrase: Optional[Phrase] = None
    phrase_expiry_date: Optional[datetime] = None
    big_advert_expiry_date: Optional[datetime] = None
    boost_expiry_date: Optional[datetime] = None


class UpdatePromotionSchema(BaseModel):
    highlight_colour: Optional[Colour] = None
    phrase: Optional[Phrase] = None
    is_boosted: Optional[bool] = None
    is_big_advert: Optional[bool] = None


class GetPromotionSchema(BaseModel):
    id: int
    highlight_colour: Optional[Colour] = None
    highlight_expiry_date: Optional[datetime] = Field(default=None, exclude=True)
    phrase: Optional[Phrase] = None
    phrase_expiry_date: Optional[datetime] = Field(default=None, exclude=True)
    big_advert_expiry_date: Optional[datetime] = Field(default=None, exclude=True)
    boost_expiry_date: Optional[datetime] = Field(default=None, exclude=True)

    @computed_field
    @property
    def is_big_advert(self) -> bool:
        now = datetime.now()
        if self.big_advert_expiry_date and self.big_advert_expiry_date < now:
            return True
        return False

    @computed_field
    @property
    def is_boosted(self) -> bool:
        now = datetime.now()
        if self.boost_expiry_date and self.boost_expiry_date < now:
            return True
        return False

    def model_post_init(self, __context):
        now = datetime.now()

        if self.highlight_expiry_date and self.highlight_expiry_date < now:
            self.highlight_colour = None

        if self.phrase_expiry_date and self.phrase_expiry_date < now:
            self.phrase = None


class GetPromotionWithExpiryDatesSchema(BaseModel):
    id: int
    highlight_colour: Optional[Colour] = None
    highlight_expiry_date: Optional[datetime] = None
    phrase: Optional[Phrase] = None
    phrase_expiry_date: Optional[datetime] = None
    big_advert_expiry_date: Optional[datetime] = None
    boost_expiry_date: Optional[datetime] = None

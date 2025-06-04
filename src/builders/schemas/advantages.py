from typing import Optional
from pydantic import BaseModel, Field


class BaseAdvantagesSchema(BaseModel):
    has_children_playground: Optional[bool] = Field(default=None)
    has_sports_field: Optional[bool] = Field(default=None)
    has_parking: Optional[bool] = Field(default=None)
    has_landscaped_area: Optional[bool] = Field(default=None)
    has_on_site_shops: Optional[bool] = Field(default=None)
    has_individual_heating: Optional[bool] = Field(default=None)
    has_balcony_or_loggia: Optional[bool] = Field(default=None)
    has_bicycle_field: Optional[bool] = Field(default=None)
    has_panoramic_windows: Optional[bool] = Field(default=None)
    is_close_to_sea: Optional[bool] = Field(default=None)
    is_close_to_school: Optional[bool] = Field(default=None)
    is_close_to_transport: Optional[bool] = Field(default=None)


class UpdateAdvantagesSchema(BaseAdvantagesSchema):
    pass


class GetAdvantagesSchema(BaseAdvantagesSchema):
    id: int

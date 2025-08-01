from pydantic import BaseModel

from .complex import GetComplexFeedListItemSchema, GetComplexFeedDetailSchema


class CreateFavouriteComplexSchema(BaseModel):
    complex_id: int


class GetFavouriteComplexListItemSchema(BaseModel):
    id: int
    complex: GetComplexFeedListItemSchema


class GetFavouriteComplexDetailSchema(BaseModel):
    id: int
    complex: GetComplexFeedDetailSchema

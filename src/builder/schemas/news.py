from typing import Optional

from pydantic import BaseModel, Field


class CreateNewsSchema(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=20, max_length=500)


class UpdateNewsSchema(BaseModel):
    title: Optional[str] = Field(min_length=5, max_length=50)
    description: Optional[str] = Field(min_length=20, max_length=500)


class GetNewsSchema(BaseModel):
    id: int
    title: str
    description: str

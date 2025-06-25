from pydantic import BaseModel, Field

from src.builders.schemas.block import GetBlockSchema


class CreateSectionSchema(BaseModel):
    block_id: int
    no: int = Field(ge=1, le=255)


class UpdateSectionSchema(BaseModel):
    block_id: int
    no: int = Field(ge=1, le=255)


class GetSectionSchema(BaseModel):
    id: int
    no: int
    block: GetBlockSchema

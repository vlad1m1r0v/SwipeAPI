from typing import Optional

from pydantic import BaseModel, Field

from src.builder.schemas.block import GetBlockSchema


class CreateFloorSchema(BaseModel):
    block_id: int
    no: int = Field(ge=1, le=255)


class UpdateFloorSchema(BaseModel):
    block_id: Optional[int] = None
    no: Optional[int] = Field(ge=1, le=255, default=None)


class GetFloorSchema(BaseModel):
    id: int
    no: int
    block: GetBlockSchema

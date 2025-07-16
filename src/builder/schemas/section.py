from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.builder.schemas.block import GetBlockSchema


class CreateSectionSchema(BaseModel):
    block_id: int
    no: int = Field(ge=1, le=255)


class UpdateSectionSchema(BaseModel):
    block_id: Optional[int] = None
    no: Optional[int] = Field(ge=1, le=255, default=None)


class GetSectionSchema(BaseModel):
    id: int
    no: int

    block: GetBlockSchema = Field(exclude=True)

    @computed_field
    @property
    def block_id(self) -> int:
        return self.block.id

    @computed_field
    @property
    def block_no(self) -> int:
        return self.block.no


class GetSectionWithComplexSchema(GetSectionSchema):
    @computed_field
    @property
    def complex_id(self) -> int:
        return self.block.complex.id

    @computed_field
    @property
    def complex_name(self) -> str:
        return self.block.complex.name

from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.builder.schemas.section import GetSectionSchema


class CreateRiserSchema(BaseModel):
    section_id: int
    no: int = Field(ge=1, le=255)


class UpdateRiserSchema(BaseModel):
    section_id: Optional[int] = None
    no: Optional[int] = Field(ge=1, le=255, default=None)


class GetRiserSchema(BaseModel):
    id: int
    no: int

    section: GetSectionSchema = Field(exclude=True)

    @computed_field
    @property
    def section_id(self) -> int:
        return self.section.id

    @computed_field
    @property
    def section_no(self) -> int:
        return self.section.no

    @computed_field
    @property
    def block_id(self) -> int:
        return self.section.block.id

    @computed_field
    @property
    def block_no(self) -> int:
        return self.section.block.no

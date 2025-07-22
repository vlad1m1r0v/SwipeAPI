from pydantic import BaseModel, Field, computed_field

from src.builder.schemas import GetComplexIdAndNoSchema


class CreateBlockSchema(BaseModel):
    no: int = Field(ge=1, le=255)


class CreateBlockWithComplexSchema(CreateBlockSchema):
    complex_id: int


class UpdateBlockSchema(BaseModel):
    no: int = Field(ge=1, le=255)


class GetBlockSchema(BaseModel):
    id: int
    no: int
    complex: GetComplexIdAndNoSchema = Field(exclude=True)


class GetBlockWithComplexSchema(GetBlockSchema):
    @computed_field
    @property
    def complex_id(self) -> int:
        return self.complex.id

    @computed_field
    @property
    def complex_name(self) -> str:
        return self.complex.name

from pydantic import BaseModel, Field


class CreateBlockSchema(BaseModel):
    no: int = Field(ge=1, le=255)


class UpdateBlockSchema(BaseModel):
    no: int = Field(ge=1, le=255)


class GetComplexSchema(BaseModel):
    id: int
    name: str


class GetBlockSchema(BaseModel):
    id: int
    no: int
    complex: GetComplexSchema = Field(exclude=True)

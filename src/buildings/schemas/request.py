from pydantic import BaseModel, Field, computed_field


class GetComplexSchema(BaseModel):
    id: int
    name: str


class GetBlockSchema(BaseModel):
    id: int
    no: int = Field(exclude=True)
    complex: GetComplexSchema = Field(exclude=True)

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.complex.name}, Block № {self.no}"


class GetSectionSchema(BaseModel):
    id: int
    no: int = Field(exclude=True)
    block: GetBlockSchema = Field(exclude=True)

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.block.name}, Section № {self.no}"


class GetFloorSchema(BaseModel):
    id: int
    no: int = Field(exclude=True)
    block: GetBlockSchema = Field(exclude=True)

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.block.name}, Floor № {self.no}"


class GetRiserSchema(BaseModel):
    id: int
    no: int = Field(exclude=True)
    section: GetSectionSchema = Field(exclude=True)

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.section.name}, Riser № {self.no}"

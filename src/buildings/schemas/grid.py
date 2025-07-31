from typing import List, Optional

from pydantic import BaseModel, Field, computed_field


class GetBlockSchema(BaseModel):
    id: int
    no: int


class GetSectionSchema(BaseModel):
    id: int
    no: int = Field(exclude=True)
    block: GetBlockSchema = Field(exclude=True)

    @computed_field
    @property
    def name(self) -> str:
        return f"Block № {self.block.no}, Section № {self.no}"


class GetRiserGridSchema(BaseModel):
    riser_id: int
    riser_no: int
    flat_id: Optional[int] = None


class GetFloorGridSchema(BaseModel):
    floor_id: int
    floor_no: int
    risers: List[GetRiserGridSchema]

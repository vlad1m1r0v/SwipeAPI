from pydantic import BaseModel


class CreateAddToComplexRequest(BaseModel):
    apartment_id: int
    riser_id: int
    floor_id: int


class GetAddToComplexRequest(BaseModel):
    id: int
    apartment_id: int
    riser_id: int
    floor_id: int

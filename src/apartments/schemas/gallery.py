from pydantic import BaseModel


class CreateImageSchema(BaseModel):
    apartment_id: int
    photo: str
    order: int

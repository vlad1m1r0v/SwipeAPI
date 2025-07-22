from pydantic import BaseModel


class CreateImageSchema(BaseModel):
    complex_id: int
    photo: str
    order: int

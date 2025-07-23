from pydantic import BaseModel


class CreateViewSchema(BaseModel):
    announcement_id: int
    user_id: int

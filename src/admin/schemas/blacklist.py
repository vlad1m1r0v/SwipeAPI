from pydantic import BaseModel


class BlacklistUserSchema(BaseModel):
    user_id: int

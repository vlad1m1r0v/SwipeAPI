from pydantic import BaseModel


class SuccessfulMessageSchema(BaseModel):
    message: str


class ErrorMessageSchema(BaseModel):
    message: str

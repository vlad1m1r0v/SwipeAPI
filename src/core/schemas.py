from typing import Optional

from pydantic import BaseModel


class SuccessfulMessageSchema(BaseModel):
    message: str


class FileInfo(BaseModel):
    filename: str
    content_type: str
    path: str
    url: Optional[str]


__all__ = [
    'SuccessfulMessageSchema',
    "FileInfo"
]

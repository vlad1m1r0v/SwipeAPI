from typing import Optional

from pydantic import BaseModel

class FileInfo(BaseModel):
    filename: str
    content_type: str
    path: str
    url: Optional[str]

__all__ = ["FileInfo"]
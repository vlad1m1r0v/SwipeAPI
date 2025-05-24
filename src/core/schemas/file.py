from pydantic import BaseModel


class FileInfo(BaseModel):
    content_path: str
    url: str
from typing import Optional

from config import config

from pydantic import BaseModel, Field, computed_field


class CreateDocumentSchema(BaseModel):
    complex_id: int
    name: str = Field(min_length=5, max_length=50)
    file: str


class UpdateDocumentSchema(BaseModel):
    name: Optional[str] = Field(min_length=5, max_length=50)
    file: Optional[str]


class GetDocumentSchema(BaseModel):
    id: int
    name: str
    file: str = Field(exclude=True)

    @computed_field
    @property
    def file_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.file}" if self.file else None

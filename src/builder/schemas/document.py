from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.core.schemas import FileInfo


class CreateDocumentSchema(BaseModel):
    name: str = Field(min_length=5, max_length=50)
    file: FileInfo


class UpdateDocumentSchema(BaseModel):
    name: Optional[str] = Field(min_length=5, max_length=50)
    file: Optional[FileInfo]


class GetDocumentSchema(BaseModel):
    id: int
    name: str
    file: FileInfo = Field(exclude=True)

    @computed_field
    @property
    def file_url(self) -> Optional[str]:
        return self.file.url if self.file else None

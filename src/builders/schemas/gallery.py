from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.core.schemas import FileInfo


class GetGalleryImageSchema(BaseModel):
    id: int
    photo: FileInfo = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return self.photo.url if self.photo else None

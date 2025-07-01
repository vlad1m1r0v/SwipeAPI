import enum
import re
from typing import Optional

from pydantic import BaseModel, Field, model_validator, computed_field

from src.core.schemas import FileInfo


class Action(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


BASE64_URL_REGEX = re.compile(
    r"^data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/]+={0,2}$"
)


class GetGalleryImageSchema(BaseModel):
    id: int
    photo: FileInfo = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return self.photo.url if self.photo else None


class MediaItem(BaseModel):
    action: Action
    id: Optional[int] = None
    base64: Optional[str] = Field(examples=["data:image/webp;base64,..."], default=None)
    order: Optional[int] = None

    @model_validator(mode="after")
    def validate_all(self) -> "MediaItem":
        if self.action == Action.CREATED and self.id is not None:
            raise ValueError("Newly created item cannot have an ID.")

        if self.action in {Action.UPDATED, Action.DELETED} and self.id is None:
            raise ValueError(f"{self.action.value.title()} item must have an ID.")

        if self.action == Action.CREATED:
            if not self.base64:
                raise ValueError("Base64 image required for newly created item.")
            if not BASE64_URL_REGEX.fullmatch(self.base64):
                raise ValueError("Invalid base64 format.")
        else:
            if self.base64:
                raise ValueError("Base64 image should only be sent for created items.")

        if self.action == Action.DELETED and self.order is not None:
            raise ValueError("Deleted item cannot have order set.")

        return self

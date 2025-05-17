import enum


class STORAGE_CONTAINER(enum.StrEnum):
    IMAGES = "images"
    DOCS = "docs"

__all__ = ["STORAGE_CONTAINER"]
import os
import uuid
from pathlib import Path
from typing import Type

from fastapi import Request, UploadFile

from sqlalchemy import event, inspect
from sqlalchemy.orm import Mapper
from advanced_alchemy.base import AdvancedDeclarativeBase

from src.core.constants import MEDIA_DIR
from src.core.schemas import FileInfo


def save_file(request: Request, file: UploadFile) -> FileInfo:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    content_path = MEDIA_DIR / filename

    with content_path.open("wb") as f:
        f.write(file.file.read())

    base_url = f"{request.url.scheme}://{request.headers['host']}"
    url = f"{base_url}/media/{filename}"

    return FileInfo(content_path=str(content_path), url=url)


def delete_file(content_path: str) -> None:
    try:
        os.remove(content_path)
    except FileNotFoundError:
        pass


def attach_file_cleanup(model_class: Type[AdvancedDeclarativeBase], fields: list[str]):
    @event.listens_for(model_class, "before_delete")
    def on_delete(_mapper: Mapper, _connection, target):
        for field in fields:
            delete_file(getattr(target, field, None))

    @event.listens_for(model_class, "before_update")
    def on_update(_mapper: Mapper, _connection, target):
        state = inspect(target)
        for field in fields:
            hist = state.attrs[field].history
            if hist.has_changes():
                old_value: FileInfo = hist.deleted[0] if hist.deleted else None
                delete_file(old_value["content_path"])

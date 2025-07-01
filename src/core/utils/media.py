import os
import io
import base64
import uuid
from pathlib import Path
from typing import Type

from starlette.datastructures import UploadFile as StarletteUploadFile
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
            file_info: FileInfo = getattr(target, field, None)
            delete_file(file_info["content_path"])

    @event.listens_for(model_class, "before_update")
    def on_update(_mapper: Mapper, _connection, target):
        state = inspect(target)
        for field in fields:
            hist = state.attrs[field].history
            if hist.has_changes():
                old_value: FileInfo = hist.deleted[0] if hist.deleted else None
                delete_file(old_value["content_path"])


def convert_base64_to_starlette_file(encoded_image: str) -> StarletteUploadFile:
    base64_str = encoded_image.split(",")[1]
    decoded = base64.b64decode(base64_str)

    file = io.BytesIO(decoded)
    file.seek(0)

    return StarletteUploadFile(file=file, filename="image.png")

import os
import io
import base64
import uuid
from pathlib import Path
from typing import Type

from starlette.datastructures import UploadFile as StarletteUploadFile
from fastapi import UploadFile

from sqlalchemy import event, inspect
from sqlalchemy.orm import Mapper
from advanced_alchemy.base import AdvancedDeclarativeBase

from src.core.constants import MEDIA_FOLDER


def save_file(file: UploadFile) -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    content_path = os.path.join(MEDIA_FOLDER, filename)

    with open(content_path, "wb") as f:
        f.write(file.file.read())

    return str(content_path)


def delete_file(content_path: str) -> None:
    try:
        os.remove(content_path)
    except FileNotFoundError:
        pass
    except TypeError:
        pass


def attach_file_cleanup(model_class: Type[AdvancedDeclarativeBase], fields: list[str]):
    @event.listens_for(model_class, "before_delete")
    def on_delete(_mapper: Mapper, _connection, target):
        for field in fields:
            file = getattr(target, field, None)
            delete_file(file)

    @event.listens_for(model_class, "before_update")
    def on_update(_mapper: Mapper, _connection, target):
        state = inspect(target)
        for field in fields:
            hist = state.attrs[field].history
            if hist.has_changes():
                old_value = hist.deleted[0] if hist.deleted else None
                delete_file(old_value)


def convert_base64_to_starlette_file(encoded_image: str) -> StarletteUploadFile:
    base64_str = encoded_image.split(",")[1]
    decoded = base64.b64decode(base64_str)

    file = io.BytesIO(decoded)
    file.seek(0)

    return StarletteUploadFile(file=file, filename="image.png")

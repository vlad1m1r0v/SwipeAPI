import os
import uuid
from pathlib import Path

from fastapi import (
    Request,
    UploadFile
)

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

    return FileInfo(
        content_path=str(content_path),
        url=url
    )


def delete_file(content_path: str) -> None:
    try:
        os.remove(content_path)
    except FileNotFoundError:
        pass

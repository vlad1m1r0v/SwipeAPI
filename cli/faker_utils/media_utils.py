from io import BytesIO
from pathlib import Path

from starlette.datastructures import UploadFile

from src.core.utils import save_file


def save_file_from_dataset(file_path: str) -> str:
    with open(file_path, "rb") as file:
        upload_file = UploadFile(
            file=BytesIO(file.read()), filename=Path(file_path).name
        )
        photo = save_file(upload_file)

    return photo

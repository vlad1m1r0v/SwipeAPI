from io import BytesIO

from starlette.datastructures import UploadFile

from src.core.utils import save_file


def save_file_from_dataset(file_path: str) -> str:
    with open(file_path, "rb") as file:
        photo = save_file(UploadFile(file=BytesIO(file.read()), filename="file"))

    return photo

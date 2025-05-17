import typing

from libcloud.storage.drivers.local import LocalStorageDriver

from sqlalchemy_file.storage import StorageManager

from src.core.constants import BASE_DIR
from src.core.enums import STORAGE_CONTAINER

MEDIA_PATH: typing.Final[str] = BASE_DIR / "media"


def setup_file_storage():
    try:
        images_container = LocalStorageDriver(MEDIA_PATH).get_container(STORAGE_CONTAINER.IMAGES)
        docs_container = LocalStorageDriver(MEDIA_PATH).get_container(STORAGE_CONTAINER.DOCS)

        StorageManager.add_storage(STORAGE_CONTAINER.IMAGES, images_container)
        StorageManager.add_storage(STORAGE_CONTAINER.DOCS, docs_container)
    except RuntimeError as _:
        pass

__all__ = ["setup_file_storage"]

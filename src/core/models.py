from advanced_alchemy.types import StoredObject

from src.core.storage_backend import local_storage


class LocalStoredObject(StoredObject):
    def __init__(self):
        super().__init__(backend=local_storage)


__all__ = ["LocalStoredObject"]
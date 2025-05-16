from advanced_alchemy.types.file_object.backends.obstore import ObstoreBackend

from src.core.constants import BASE_DIR

local_storage = ObstoreBackend(
    key="local",
    fs=f"file:///{BASE_DIR}/media/",
)

__all__ = ["local_storage"]

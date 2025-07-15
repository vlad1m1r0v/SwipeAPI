import typing
from pathlib import Path

# BASE_DIR / src / core / constants / dirs.py
BASE_DIR: typing.Final = Path(__file__).parent.parent.parent.parent
# BASE_DIR / MEDIA_FOLDER
MEDIA_FOLDER = "media"
MEDIA_DIR: typing.Final = BASE_DIR / MEDIA_FOLDER
DATASETS_DIR: typing.Final = BASE_DIR / "datasets"

__all__ = ["BASE_DIR", "MEDIA_DIR", "MEDIA_FOLDER", "DATASETS_DIR"]

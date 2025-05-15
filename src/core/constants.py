import typing
from pathlib import Path

BASE_DIR: typing.Final =Path(__file__).parent.parent.parent

__all__ = ['BASE_DIR']
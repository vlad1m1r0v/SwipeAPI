from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    message: Optional[str] = None
    data: Optional[T] = None

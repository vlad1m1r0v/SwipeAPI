from enum import Enum

from typing import TypeVar, Generic, Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.generics import GenericModel

from starlette import status

T = TypeVar("T")


class SuccessStatus(str, Enum):
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    INFO = "INFO"
    DANGER = "DANGER"


class SuccessDetails(GenericModel, Generic[T]):
    value: Optional[T] = None
    message: Optional[str] = None


class SuccessData(GenericModel, Generic[T]):
    success_status: SuccessStatus = Field(default=SuccessStatus.SUCCESS)
    details: SuccessDetails[T]


class SuccessResponse(GenericModel, Generic[T]):
    status: int = Field(default=status.HTTP_200_OK)
    data: SuccessData[T]

    model_config = ConfigDict(exclude_none=True)


def success_response(
    value: Optional[T] = None,
    message: Optional[str] = None,
    success_status: SuccessStatus = SuccessStatus.SUCCESS,
    status_code: int = status.HTTP_200_OK,
) -> SuccessResponse[T]:
    return SuccessResponse[T](
        status=status_code,
        data=SuccessData[T](
            success_status=success_status,
            details=SuccessDetails[T](value=value, message=message),
        ),
    )


# TODO: remove
class SuccessfulMessageSchema(BaseModel):
    message: str


# TODO: remove
class ErrorMessageSchema(BaseModel):
    message: str

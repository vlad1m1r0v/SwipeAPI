from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.requests.models import AddToComplexRequest
from src.requests.services import AddToComplexRequestService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_request(
    request_id: int,
    request_service: FromDishka[AddToComplexRequestService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    request = await request_service.get(
        request_id, load=[orm.joinedload(AddToComplexRequest.apartment)]
    )

    print(request.apartment.user_id, user.id)

    if request.apartment.user_id != user.id:
        raise IsNotOwnerException()

    return user

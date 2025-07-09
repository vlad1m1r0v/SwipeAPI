from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.apartments.services import ApartmentService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_apartment(
    apartment_id: int,
    apartment_service: FromDishka[ApartmentService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    apartment = await apartment_service.get(item_id=apartment_id)

    if apartment.user_id != user.id:
        raise IsNotOwnerException()

    return user

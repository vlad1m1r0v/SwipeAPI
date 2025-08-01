from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.builder.services import FavouriteComplexService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_favourite_complex(
    favourite_id: int,
    favourite_complex_service: FromDishka[FavouriteComplexService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    favourite_complex = await favourite_complex_service.get(item_id=favourite_id)

    if favourite_complex.user_id != user.id:
        raise IsNotOwnerException()

    return user

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import builder_from_token

from src.builders.services import AdvantagesService
from src.builders.schemas import UpdateAdvantagesSchema, GetBuilderSchema

from src.users.services import UserService

router = APIRouter()


@router.patch("/advantages")
@inject
async def update_advantages(
    advantages_service: FromDishka[AdvantagesService],
    user_service: FromDishka[UserService],
    data: Annotated[UpdateAdvantagesSchema, Form()],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await advantages_service.update(data=data, item_id=builder.complex.advantages.id)
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import builder_from_token

from src.builders.services import InfrastructureService
from src.builders.schemas import UpdateInfrastructureSchema, GetBuilderSchema

from src.users.services import UserService

router = APIRouter()


@router.patch("/infrastructure")
@inject
async def update_infrastructure(
    infrastructure_service: FromDishka[InfrastructureService],
    user_service: FromDishka[UserService],
    data: Annotated[UpdateInfrastructureSchema, Form()],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await infrastructure_service.update(
        data=data, item_id=builder.complex.infrastructure.id
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)

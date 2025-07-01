from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.auth.dependencies import builder_from_token

from src.builder.services import InfrastructureService
from src.builder.schemas import UpdateInfrastructureSchema, GetBuilderSchema

from src.user.services import UserService

router = APIRouter()


@router.patch("/infrastructure", tags=["Builder: Profile"])
@inject
async def update_infrastructure(
    infrastructure_service: FromDishka[InfrastructureService],
    user_service: FromDishka[UserService],
    data: UpdateInfrastructureSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await infrastructure_service.update(
        data=data, item_id=builder.complex.infrastructure.id
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)

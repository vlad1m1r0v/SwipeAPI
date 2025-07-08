from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import builder_from_token

from src.builder.services import AdvantagesService
from src.builder.schemas import (
    GetAdvantagesSchema,
    UpdateAdvantagesSchema,
    GetBuilderSchema,
)

router = APIRouter()


@router.patch(
    path="/advantages",
    response_model=SuccessResponse[GetAdvantagesSchema],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    tags=["Builder: Profile"],
)
@inject
async def update_advantages(
    advantages_service: FromDishka[AdvantagesService],
    data: UpdateAdvantagesSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetAdvantagesSchema]:
    data = await advantages_service.update(
        data=data, item_id=builder.complex.advantages.id
    )
    return SuccessResponse(
        data=advantages_service.to_schema(data=data, schema_type=GetAdvantagesSchema)
    )

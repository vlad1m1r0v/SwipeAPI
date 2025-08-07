from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse
from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)

from src.auth.dependencies import builder_from_token

from src.builder.services import InfrastructureService
from src.builder.schemas import (
    GetInfrastructureSchema,
    UpdateInfrastructureSchema,
    GetBuilderSchema,
)

router = APIRouter()


@router.patch(
    path="/infrastructure",
    response_model=SuccessResponse[GetInfrastructureSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def update_infrastructure(
    infrastructure_service: FromDishka[InfrastructureService],
    data: UpdateInfrastructureSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetInfrastructureSchema]:
    data = await infrastructure_service.update(
        data=data, item_id=builder.complex.infrastructure.id
    )
    return SuccessResponse(
        data=infrastructure_service.to_schema(
            data=data, schema_type=GetInfrastructureSchema
        )
    )

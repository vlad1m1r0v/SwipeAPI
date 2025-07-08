from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples
from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)

from src.builder.schemas import (
    GetBuilderSchema,
    GetFloorSchema,
    UpdateFloorSchema,
    CreateFloorSchema,
)
from src.builder.services import FloorService
from src.builder.dependencies import check_builder_owns_floor

from src.auth.dependencies import builder_from_token

router = APIRouter(prefix="/floors", tags=["Builder: Floors"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetFloorSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_floors(
    floor_service: FromDishka[FloorService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    block_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[GetFloorSchema]]:
    results, total = await floor_service.get_floors(
        limit=limit,
        offset=offset,
        complex_id=builder.complex.id,
        block_id=block_id,
        no=no,
    )
    return SuccessResponse(
        data=floor_service.to_schema(
            data=results, total=total, schema_type=GetFloorSchema
        )
    )


@router.post(
    path="",
    response_model=SuccessResponse[GetFloorSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_floor(
    floor_service: FromDishka[FloorService],
    data: CreateFloorSchema = Body(),
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetFloorSchema]:
    floor = await floor_service.create(data=data.model_dump())
    return SuccessResponse(
        data=floor_service.to_schema(data=floor, schema_type=GetFloorSchema)
    )


@router.patch(
    path="/{floor_id}",
    response_model=SuccessResponse[GetFloorSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_floor(
    floor_service: FromDishka[FloorService],
    floor_id: int,
    data: UpdateFloorSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_floor),
) -> SuccessResponse[GetFloorSchema]:
    floor = await floor_service.update(
        item_id=floor_id, data=data.model_dump(exclude_none=True)
    )
    return SuccessResponse(
        data=floor_service.to_schema(data=floor, schema_type=GetFloorSchema)
    )


@router.delete(
    path="/{floor_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_floor(
    floor_service: FromDishka[FloorService],
    floor_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_floor),
):
    await floor_service.delete(item_id=floor_id)
    return SuccessResponse(message="Floor has been deleted successfully.")

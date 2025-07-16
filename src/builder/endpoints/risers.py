from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.schemas import (
    GetBuilderSchema,
    GetRiserSchema,
    GetRiserWithComplexSchema,
    UpdateRiserSchema,
    CreateRiserSchema,
)
from src.builder.services import RiserService
from src.builder.dependencies import check_builder_owns_riser

from src.auth.dependencies import builder_from_token, user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/risers", tags=["Builder: Risers"])
risers = APIRouter(prefix="/risers", tags=["User: Add to complex requests"])


@risers.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetRiserWithComplexSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_risers(
    riser_service: FromDishka[RiserService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    block_id: int | None = Query(default=None),
    section_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetRiserWithComplexSchema]]:
    results, total = await riser_service.get_risers(
        limit=limit,
        offset=offset,
        complex_id=complex_id,
        block_id=block_id,
        section_id=section_id,
        no=no,
    )
    return SuccessResponse(
        data=riser_service.to_schema(
            data=results, total=total, schema_type=GetRiserWithComplexSchema
        )
    )


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetRiserSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_complex_risers(
    riser_service: FromDishka[RiserService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    block_id: int | None = Query(default=None),
    section_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[GetRiserSchema]]:
    results, total = await riser_service.get_risers(
        limit=limit,
        offset=offset,
        complex_id=builder.complex.id,
        block_id=block_id,
        section_id=section_id,
        no=no,
    )
    return SuccessResponse(
        data=riser_service.to_schema(
            data=results, total=total, schema_type=GetRiserSchema
        )
    )


@router.post(
    path="",
    response_model=SuccessResponse[GetRiserSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_riser(
    riser_service: FromDishka[RiserService],
    data: CreateRiserSchema = Body(),
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetRiserSchema]:
    created = await riser_service.create(data=data.model_dump())
    riser = await riser_service.get_riser(item_id=created.id)
    return SuccessResponse(
        data=riser_service.to_schema(data=riser, schema_type=GetRiserSchema)
    )


@router.patch(
    path="/{riser_id}",
    response_model=SuccessResponse[GetRiserSchema],
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
async def update_riser(
    riser_service: FromDishka[RiserService],
    riser_id: int,
    data: UpdateRiserSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_riser),
) -> SuccessResponse[GetRiserSchema]:
    updated = await riser_service.update(
        item_id=riser_id, data=data.model_dump(exclude_none=True)
    )
    riser = await riser_service.get_riser(item_id=updated.id)
    return SuccessResponse(
        data=riser_service.to_schema(data=riser, schema_type=GetRiserSchema)
    )


@router.delete(
    path="/{riser_id}",
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
async def delete_riser(
    riser_service: FromDishka[RiserService],
    riser_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_riser),
) -> SuccessResponse:
    await riser_service.delete(item_id=riser_id)
    return SuccessResponse(message="Riser has been deleted successfully.")

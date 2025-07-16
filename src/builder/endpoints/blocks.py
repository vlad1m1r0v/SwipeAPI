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
    GetBlockSchema,
    GetBlockWithComplexSchema,
    CreateBlockSchema,
    UpdateBlockSchema,
)
from src.builder.services import BlockService
from src.builder.dependencies import check_builder_owns_block

from src.auth.dependencies import builder_from_token, user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/blocks", tags=["Builder: Blocks"])
blocks = APIRouter(
    prefix="/add-to-complex-request/blocks", tags=["User: Add to complex requests"]
)


@blocks.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetBlockWithComplexSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_blocks(
    block_service: FromDishka[BlockService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetBlockWithComplexSchema]]:
    results, total = await block_service.get_blocks(
        limit=limit, offset=offset, complex_id=complex_id, no=no
    )
    return SuccessResponse(
        data=block_service.to_schema(
            data=results, total=total, schema_type=GetBlockWithComplexSchema
        )
    )


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetBlockSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_complex_blocks(
    block_service: FromDishka[BlockService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[GetBlockSchema]]:
    results, total = await block_service.get_blocks(
        limit=limit, offset=offset, complex_id=builder.complex.id, no=no
    )
    return SuccessResponse(
        data=block_service.to_schema(
            data=results, total=total, schema_type=GetBlockSchema
        )
    )


@router.post(
    path="",
    response_model=SuccessResponse[GetBlockSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_block(
    block_service: FromDishka[BlockService],
    data: CreateBlockSchema = Body(),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetBlockSchema]:
    created = await block_service.create(
        data={**data.model_dump(), "complex_id": builder.complex.id}
    )
    block = await block_service.get_block(created.id)

    return SuccessResponse(
        data=block_service.to_schema(data=block, schema_type=GetBlockSchema)
    )


@router.patch(
    path="/{block_id}",
    response_model=SuccessResponse[GetBlockSchema],
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
async def update_block(
    block_service: FromDishka[BlockService],
    block_id: int,
    data: UpdateBlockSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_block),
) -> SuccessResponse[GetBlockSchema]:
    updated = await block_service.update(item_id=block_id, data=data.model_dump())
    block = await block_service.get_block(updated.id)

    return SuccessResponse(
        data=block_service.to_schema(data=block, schema_type=GetBlockSchema)
    )


@router.delete(
    path="/{block_id}",
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
async def delete_block(
    block_service: FromDishka[BlockService],
    block_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_block),
):
    await block_service.delete(item_id=block_id)
    return SuccessResponse(message="Block has been deleted successfully.")

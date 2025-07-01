from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessfulMessageSchema

from src.builder.schemas import (
    GetBuilderSchema,
    GetBlockSchema,
    CreateBlockSchema,
    UpdateBlockSchema,
)
from src.builder.services import BlockService
from src.builder.dependencies import check_builder_owns_block

from src.auth.dependencies import builder_from_token

router = APIRouter(prefix="/blocks", tags=["Builder: Blocks"])


@router.get("", response_model=OffsetPagination[GetBlockSchema])
@inject
async def get_blocks(
    block_service: FromDishka[BlockService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> OffsetPagination[GetBlockSchema]:
    results, total = await block_service.get_blocks(
        limit=limit, offset=offset, complex_id=builder.complex.id, no=no
    )
    return block_service.to_schema(
        data=results, total=total, schema_type=GetBlockSchema
    )


@router.post("", response_model=SuccessfulMessageSchema)
@inject
async def create_block(
    block_service: FromDishka[BlockService],
    data: CreateBlockSchema = Body(),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessfulMessageSchema:
    await block_service.create(
        data={**data.model_dump(), "complex_id": builder.complex.id}
    )
    return SuccessfulMessageSchema(
        message="Block has been added successfully to complex."
    )


@router.patch("/{block_id}", response_model=SuccessfulMessageSchema)
@inject
async def update_block(
    block_service: FromDishka[BlockService],
    block_id: int,
    data: UpdateBlockSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_block),
) -> SuccessfulMessageSchema:
    await block_service.update(item_id=block_id, data=data.model_dump())
    return SuccessfulMessageSchema(message="Block has been updated successfully.")


@router.delete("/{block_id}", response_model=SuccessfulMessageSchema)
@inject
async def delete_block(
    block_service: FromDishka[BlockService],
    block_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_block),
):
    await block_service.delete(item_id=block_id)
    return SuccessfulMessageSchema(message="Block has been deleted successfully.")

from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.builder.services import BlockService

from src.auth.dependencies import builder_from_token

from src.builder.schemas import GetBuilderSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_block(
    block_id: int,
    block_service: FromDishka[BlockService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    block = await block_service.get(item_id=block_id)

    if block.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder

from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.builders.services import FloorService
from src.builders.models import Floor
from src.builders.schemas import GetBuilderSchema

from src.auth.dependencies import builder_from_token

from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_floor(
    floor_id: int,
    floor_service: FromDishka[FloorService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    floor = await floor_service.get(
        item_id=floor_id, load=[orm.joinedload(Floor.block)]
    )

    if floor.block.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder

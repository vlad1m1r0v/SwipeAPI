from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.builder.services import RiserService
from src.builder.models import Riser, Section
from src.builder.schemas import GetBuilderSchema

from src.auth.dependencies import builder_from_token

from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_riser(
    riser_id: int,
    riser_service: FromDishka[RiserService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    riser = await riser_service.get(
        item_id=riser_id, load=[orm.joinedload(Riser.section).joinedload(Section.block)]
    )

    if riser.section.block.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder

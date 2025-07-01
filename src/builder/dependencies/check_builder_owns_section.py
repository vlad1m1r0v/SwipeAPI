from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.builder.services import SectionService
from src.builder.models import Section
from src.builder.schemas import GetBuilderSchema

from src.auth.dependencies import builder_from_token

from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_section(
    section_id: int,
    section_service: FromDishka[SectionService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    section = await section_service.get(
        item_id=section_id, load=[orm.joinedload(Section.block)]
    )

    if section.block.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder

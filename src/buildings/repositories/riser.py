from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Complex

from src.buildings.models import Block, Section, Riser


class RiserRepository(SQLAlchemyAsyncRepository[Riser]):
    model_type = Riser

    async def get_risers_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        section_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Riser], int]:
        section_alias = aliased(Section)
        block_alias = aliased(Block)
        complex_alias = aliased(Complex)

        stmt = select(Riser).options(
            joinedload(Riser.section.of_type(section_alias))
            .joinedload(section_alias.block.of_type(block_alias))
            .joinedload(block_alias.complex.of_type(complex_alias))
        )

        if complex_id:
            stmt = stmt.where(complex_alias.id == complex_id)

        if block_id:
            stmt = stmt.where(block_alias.id == block_id)

        if section_id:
            stmt = stmt.where(section_alias.id == section_id)

        if no:
            stmt = stmt.where(Riser.no == no)

        stmt = (
            stmt.order_by(
                complex_alias.id.asc(),
                block_alias.no.asc(),
                section_alias.no.asc(),
                Riser.no.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        results, total = await self.list_and_count(statement=stmt)
        return results, total

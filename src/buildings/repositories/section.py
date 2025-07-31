from typing import Sequence

from sqlalchemy import select, orm
from sqlalchemy.orm import aliased, joinedload

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Complex

from src.buildings.models import Block, Section


class SectionRepository(SQLAlchemyAsyncRepository[Section]):
    model_type = Section

    async def get_sections_for_grid(self, block_id: int) -> Sequence[Section]:
        stmt = (
            select(Section)
            .where(Section.block_id == block_id)
            .options(orm.joinedload(Section.block))
        )

        result = await self.session.execute(stmt)
        sections: Sequence[Section] = result.scalars().all()
        return sections

    async def get_sections_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Section], int]:
        block_alias = aliased(Block)

        stmt = select(Section).options(
            joinedload(Section.block.of_type(block_alias)).joinedload(
                block_alias.complex
            )
        )

        if complex_id:
            stmt = stmt.where(Complex.id == complex_id)

        if block_id:
            stmt = stmt.where(Section.block_id == block_id)

        if no:
            stmt = stmt.where(Section.no == no)

        stmt = (
            stmt.order_by(block_alias.no.asc(), Section.no.asc())
            .limit(limit)
            .offset(offset)
        )

        results, total = await self.list_and_count(statement=stmt)
        return results, total

from typing import Sequence


from sqlalchemy import select, orm
from sqlalchemy.orm import joinedload, aliased

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Complex, Block, Section


class SectionRepository(SQLAlchemyAsyncRepository[Section]):
    model_type = Section

    async def get_sections(
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

    async def get_section(self, item_id: int) -> Section:
        stmt = (
            select(Section)
            .where(Section.id == item_id)
            .options(orm.joinedload(Section.block))
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

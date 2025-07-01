from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

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
        stmt = select(Section).options(
            joinedload(Section.block).joinedload(Block.complex)
        )

        if complex_id:
            stmt = stmt.where(Complex.id == complex_id)

        if block_id:
            stmt = stmt.where(Section.block_id == block_id)

        if no:
            stmt = stmt.where(Section.no == no)

        stmt = stmt.order_by(Section.no.asc()).limit(limit).offset(offset)

        results, total = await self.list_and_count(statement=stmt)
        return results, total

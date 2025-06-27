from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import Complex, Block, Floor


class FloorRepository(SQLAlchemyAsyncRepository[Floor]):
    model_type = Floor

    async def get_floors(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Floor], int]:
        stmt = select(Floor).options(joinedload(Floor.block).joinedload(Block.complex))

        if complex_id:
            stmt = stmt.where(Complex.id == complex_id)

        if block_id:
            stmt = stmt.where(Floor.block_id == block_id)

        if no:
            stmt = stmt.where(Floor.no == no)

        stmt = stmt.order_by(Floor.no.asc()).limit(limit).offset(offset)

        results, total = await self.list_and_count(statement=stmt)
        return results, total

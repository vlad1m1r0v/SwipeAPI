from typing import Sequence


from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Complex

from src.buildings.models import Block, Floor


class FloorRepository(SQLAlchemyAsyncRepository[Floor]):
    model_type = Floor

    async def get_floors_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Floor], int]:
        block_alias = aliased(Block)

        stmt = select(Floor).options(
            joinedload(Floor.block.of_type(block_alias)).joinedload(block_alias.complex)
        )

        if complex_id:
            stmt = stmt.where(Complex.id == complex_id)

        if block_id:
            stmt = stmt.where(Floor.block_id == block_id)

        if no:
            stmt = stmt.where(Floor.no == no)

        stmt = (
            stmt.order_by(block_alias.no.asc(), Floor.no.asc())
            .limit(limit)
            .offset(offset)
        )

        results, total = await self.list_and_count(statement=stmt)
        return results, total

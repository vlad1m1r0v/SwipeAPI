from typing import Sequence

from sqlalchemy import select, orm

from advanced_alchemy.filters import (
    StatementFilter,
    LimitOffset,
    ComparisonFilter,
    OrderBy,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Block


class BlockRepository(SQLAlchemyAsyncRepository[Block]):
    model_type = Block

    async def get_blocks(
        self, limit: int, offset: int, complex_id: int | None, no: int | None
    ) -> tuple[Sequence[Block], int]:
        filters: list[StatementFilter] = [
            LimitOffset(limit=limit, offset=offset),
            OrderBy("no", "asc"),
        ]

        if complex_id:
            filters.append(
                ComparisonFilter(
                    field_name="complex_id", operator="eq", value=complex_id
                )
            )

        if no:
            filters.append(ComparisonFilter(field_name="no", operator="eq", value=no))

        results, total = await self.list_and_count(
            *filters, load=[orm.joinedload(Block.complex)]
        )
        return results, total

    async def get_block(self, item_id: int) -> Block:
        stmt = (
            select(Block)
            .where(Block.id == item_id)
            .options(orm.joinedload(Block.complex))
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

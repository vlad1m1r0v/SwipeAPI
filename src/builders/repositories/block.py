from typing import Sequence

from advanced_alchemy.filters import LimitOffset, ComparisonFilter, OrderBy
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import Block


class BlockRepository(SQLAlchemyAsyncRepository[Block]):
    model_type = Block

    async def get_complex_blocks(
        self, limit: int, offset: int, no: int, complex_id: int
    ) -> tuple[Sequence[Block], int]:
        filters = [
            LimitOffset(limit=limit, offset=offset),
            ComparisonFilter(field_name="complex_id", operator="eq", value=complex_id),
            OrderBy("no", "asc"),
        ]

        if no:
            filters.append(ComparisonFilter(field_name="no", operator="eq", value=no))

        results, total = await self.list_and_count(*filters)

        return results, total

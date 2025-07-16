from typing import Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset, SearchFilter

from src.builder.models import Complex


class ComplexRepository(SQLAlchemyAsyncRepository[Complex]):
    model_type = Complex

    async def get_complexes_for_filters(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[Complex], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)
        search_filter = SearchFilter(
            field_name="name",
            value=search,
            ignore_case=True,
        )

        results, total = await self.list_and_count(
            limit_offset,
            search_filter,
        )

        return results, total

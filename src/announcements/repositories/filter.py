from typing import Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import ComparisonFilter, LimitOffset

from sqlalchemy import select, func

from src.announcements.models import Filter
from src.announcements.constants import FILTERS_MAX
from src.announcements.exceptions import FiltersAmountExceededException


class AnnouncementFilterRepository(SQLAlchemyAsyncRepository[Filter]):
    model_type = Filter

    async def create_filter(self, user_id: int, data: dict) -> Filter:
        stmt = select(func.count(Filter.id)).where(Filter.user_id == user_id)
        result = await self.session.execute(stmt)
        count = result.scalar_one()

        if count >= FILTERS_MAX:
            raise FiltersAmountExceededException()

        created = await self.add(Filter(**data))
        return created

    async def get_user_filters(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[Filter], int]:
        filters = [
            LimitOffset(offset=offset, limit=limit),
            ComparisonFilter(field_name="user_id", operator="eq", value=user_id),
        ]

        return await self.list_and_count(*filters)

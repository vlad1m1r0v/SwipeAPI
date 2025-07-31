from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.buildings.models import Section
from src.buildings.repositories import SectionRepository


class SectionService(SQLAlchemyAsyncRepositoryService[Section, SectionRepository]):
    repository_type = SectionRepository

    async def get_sections_for_grid(self, block_id: int) -> Sequence[Section]:
        return await self.repository.get_sections_for_grid(block_id)

    async def get_sections_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Section], int]:
        return await self.repository.get_sections_for_requests(
            limit, offset, complex_id, block_id, no
        )

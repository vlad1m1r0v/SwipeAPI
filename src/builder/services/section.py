from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Section
from src.builder.repositories import SectionRepository


class SectionService(SQLAlchemyAsyncRepositoryService[Section, SectionRepository]):
    repository_type = SectionRepository

    async def get_sections(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Section], int]:
        return await self.repository.get_sections(
            limit, offset, complex_id, block_id, no
        )

    async def get_section(self, item_id: int) -> Section:
        return await self.repository.get_section(item_id)

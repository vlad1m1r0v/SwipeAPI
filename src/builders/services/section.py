from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Section
from src.builders.repositories import SectionRepository


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

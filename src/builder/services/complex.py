from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Complex
from src.builder.repositories import ComplexRepository


class ComplexService(SQLAlchemyAsyncRepositoryService[Complex, ComplexRepository]):
    repository_type = ComplexRepository

    async def get_complexes_for_filters(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[Complex], int]:
        return await self.repository.get_complexes_for_filters(limit, offset, search)

from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Complex
from src.builder.repositories import ComplexRepository


class ComplexService(SQLAlchemyAsyncRepositoryService[Complex, ComplexRepository]):
    repository_type = ComplexRepository

    async def get_complexes_for_requests(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[Complex], int]:
        return await self.repository.get_complexes_for_requests(limit, offset, search)

    async def get_complexes_for_feed_list(
        self, limit: int, offset: int
    ) -> tuple[Sequence[Complex], int]:
        return await self.repository.get_complexes_for_feed_list(limit, offset)

    async def get_complex_detail(self, complex_id: int) -> Complex:
        return await self.repository.get_complex_detail(complex_id)

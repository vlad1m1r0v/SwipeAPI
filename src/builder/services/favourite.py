from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import FavouriteComplex
from src.builder.repositories import FavouriteComplexRepository


class FavouriteComplexService(
    SQLAlchemyAsyncRepositoryService[FavouriteComplex, FavouriteComplexRepository]
):
    repository_type = FavouriteComplexRepository

    async def get_favourite_complexes(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[FavouriteComplex], int]:
        return await self.repository.get_favourite_complexes(
            user_id=user_id, limit=limit, offset=offset
        )

    async def get_favourite_complex_detail(self, favourite_id: int) -> FavouriteComplex:
        return await self.repository.get_favourite_complex_detail(
            favourite_id=favourite_id
        )

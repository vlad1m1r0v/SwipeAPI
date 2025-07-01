from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Floor
from src.builder.repositories import FloorRepository


class FloorService(SQLAlchemyAsyncRepositoryService[Floor, FloorRepository]):
    repository_type = FloorRepository

    async def get_floors(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Floor], int]:
        return await self.repository.get_floors(limit, offset, complex_id, block_id, no)

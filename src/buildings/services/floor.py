from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.buildings.models import Floor
from src.buildings.repositories import FloorRepository


class FloorService(SQLAlchemyAsyncRepositoryService[Floor, FloorRepository]):
    repository_type = FloorRepository

    async def get_floors_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Floor], int]:
        return await self.repository.get_floors_for_requests(
            limit, offset, complex_id, block_id, no
        )

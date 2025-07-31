from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.buildings.models import Riser
from src.buildings.repositories import RiserRepository


class RiserService(SQLAlchemyAsyncRepositoryService[Riser, RiserRepository]):
    repository_type = RiserRepository

    async def get_risers_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        block_id: int | None,
        section_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Riser], int]:
        return await self.repository.get_risers_for_requests(
            limit, offset, complex_id, block_id, section_id, no
        )

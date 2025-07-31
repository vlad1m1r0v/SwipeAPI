from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.buildings.models import Block
from src.buildings.repositories import BlockRepository


class BlockService(SQLAlchemyAsyncRepositoryService[Block, BlockRepository]):
    repository_type = BlockRepository

    async def get_blocks_for_requests(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Block], int]:
        return await self.repository.get_blocks_for_requests(
            limit, offset, complex_id, no
        )

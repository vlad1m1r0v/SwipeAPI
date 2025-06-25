from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Block
from src.builders.repositories import BlockRepository


class BlockService(SQLAlchemyAsyncRepositoryService[Block, BlockRepository]):
    repository_type = BlockRepository

    async def get_complex_blocks(
        self, limit: int, offset: int, no: int, complex_id: int
    ) -> tuple[Sequence[Block], int]:
        return await self.repository.get_complex_blocks(limit, offset, no, complex_id)

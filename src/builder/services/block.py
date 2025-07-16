from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Block
from src.builder.repositories import BlockRepository


class BlockService(SQLAlchemyAsyncRepositoryService[Block, BlockRepository]):
    repository_type = BlockRepository

    async def get_blocks(
        self,
        limit: int,
        offset: int,
        complex_id: int | None,
        no: int | None,
    ) -> tuple[Sequence[Block], int]:
        return await self.repository.get_blocks(limit, offset, complex_id, no)

    async def get_block(self, item_id: int) -> Block:
        return await self.repository.get_block(item_id)

from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.apartments.models import AddToComplexRequest
from src.apartments.repositories import AddToComplexRequestRepository


class AddToComplexRequestService(
    SQLAlchemyAsyncRepositoryService[AddToComplexRequest, AddToComplexRequestRepository]
):
    repository_type = AddToComplexRequestRepository

    async def approve(self, item_id) -> None:
        return await self.repository.approve(item_id)

    async def get_requests(
        self, limit: int, offset: int, complex_id: int
    ) -> tuple[Sequence[AddToComplexRequest], int]:
        return await self.repository.get_requests(
            limit=limit, offset=offset, complex_id=complex_id
        )

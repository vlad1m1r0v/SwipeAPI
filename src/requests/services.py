from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.requests.models import AddToComplexRequest

from src.requests.repositories import AddToComplexRequestRepository


class AddToComplexRequestService(
    SQLAlchemyAsyncRepositoryService[AddToComplexRequest, AddToComplexRequestRepository]
):
    repository_type = AddToComplexRequestRepository

    async def approve(self, item_id) -> None:
        return await self.repository.approve(item_id)

    async def get_requests_for_builder(
        self, limit: int, offset: int, complex_id: int
    ) -> tuple[Sequence[AddToComplexRequest], int]:
        return await self.repository.get_requests_for_builder(
            limit=limit, offset=offset, complex_id=complex_id
        )

    async def get_requests_for_user(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[AddToComplexRequest, int]:
        return await self.repository.get_requests_for_user(
            limit=limit, offset=offset, user_id=user_id
        )

    async def get_user_request(self, request_id: int) -> AddToComplexRequest:
        return await self.repository.get_user_request(request_id)

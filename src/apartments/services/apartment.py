from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.apartments.models import Apartment
from src.apartments.repositories import ApartmentRepository
from src.apartments.schemas import CreateApartmentSchema, UpdateApartmentSchema


class ApartmentService(
    SQLAlchemyAsyncRepositoryService[Apartment, ApartmentRepository]
):
    repository_type = ApartmentRepository

    async def get_apartment_details(self, apartment_id: int) -> Apartment:
        return await self.repository.get_apartment_details(apartment_id)

    async def get_apartments(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[Sequence[Apartment], int]:
        return await self.repository.get_apartments(
            limit=limit, offset=offset, user_id=user_id
        )

    async def create_apartment(
        self, user_id: int, data: CreateApartmentSchema
    ) -> Apartment:
        return await self.repository.create_apartment(user_id=user_id, data=data)

    async def update_apartment(
        self, item_id: int, data: UpdateApartmentSchema
    ) -> Apartment:
        return await self.repository.update_apartment(item_id=item_id, data=data)

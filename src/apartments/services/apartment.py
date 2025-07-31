from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.apartments.models import Apartment
from src.apartments.repositories import ApartmentRepository
from src.apartments.schemas import CreateApartmentSchema, UpdateApartmentSchema


class ApartmentService(
    SQLAlchemyAsyncRepositoryService[Apartment, ApartmentRepository]
):
    repository_type = ApartmentRepository

    async def get_apartments_list_for_grid(
        self,
        section_id: int,
        price_min: int | None = None,
        price_max: int | None = None,
        price_min_per_m2: int | None = None,
        price_max_per_m2: int | None = None,
        area_min: int | None = None,
        area_max: int | None = None,
        finishing: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[Sequence[Apartment], int]:
        return await self.repository.get_apartments_list_for_grid(
            section_id=section_id,
            price_min=price_min,
            price_max=price_max,
            price_min_per_m2=price_min_per_m2,
            price_max_per_m2=price_max_per_m2,
            area_min=area_min,
            area_max=area_max,
            finishing=finishing,
            limit=limit,
            offset=offset,
        )

    async def get_apartment_detail_for_grid(self, apartment_id) -> Apartment:
        return await self.repository.get_apartment_detail_for_grid(apartment_id)

    async def get_apartment_detail_for_user(self, apartment_id: int) -> Apartment:
        return await self.repository.get_apartment_detail_for_user(apartment_id)

    async def get_apartments_list_for_user(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[Sequence[Apartment], int]:
        return await self.repository.get_apartments_list_for_user(
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

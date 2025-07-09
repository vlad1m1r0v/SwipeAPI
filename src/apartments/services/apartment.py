from fastapi import Request

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.apartments.models import Apartment
from src.apartments.repositories import ApartmentRepository
from src.apartments.schemas import CreateApartmentSchema


class ApartmentService(
    SQLAlchemyAsyncRepositoryService[Apartment, ApartmentRepository]
):
    repository_type = ApartmentRepository

    async def get_apartment_details(self, apartment_id: int) -> Apartment:
        return await self.repository.get_apartment_details(apartment_id)

    async def create_apartment(
        self, request: Request, user_id: int, data: CreateApartmentSchema
    ) -> Apartment:
        return await self.repository.create_apartment(
            request=request, user_id=user_id, data=data
        )

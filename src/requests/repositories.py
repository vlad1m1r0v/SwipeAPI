from typing import Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from sqlalchemy import select, update, orm
from sqlalchemy.orm import aliased

from src.buildings.models import Block, Floor

from src.requests.models import AddToComplexRequest

from src.apartments.models import Apartment

from src.builder.models import Complex

from src.user.models import User


class AddToComplexRequestRepository(SQLAlchemyAsyncRepository[AddToComplexRequest]):
    model_type = AddToComplexRequest

    async def approve(self, item_id) -> None:
        request: AddToComplexRequest = await self.get(item_id)

        stmt = (
            update(Apartment)
            .where(Apartment.id == request.apartment_id)
            .values(floor_id=request.floor_id, riser_id=request.riser_id)
        )

        await self.session.execute(stmt)

        await self.delete(item_id=request.id)

    async def get_requests_for_builder(
        self, limit: int, offset: int, complex_id: int
    ) -> tuple[Sequence[AddToComplexRequest], int]:
        complex_alias = aliased(Complex)

        stmt = (
            select(AddToComplexRequest)
            .where(complex_alias.id == complex_id)
            .options(
                orm.joinedload(AddToComplexRequest.floor)
                .joinedload(Floor.block)
                .joinedload(Block.complex.of_type(complex_alias)),
                orm.joinedload(AddToComplexRequest.riser),
                orm.joinedload(AddToComplexRequest.apartment)
                .joinedload(Apartment.user)
                .joinedload(User.contact),
                orm.joinedload(AddToComplexRequest.apartment).selectinload(
                    Apartment.gallery
                ),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self.list_and_count(
            limit_offset,
            statement=stmt,
        )

        return results, total

    async def get_requests_for_user(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[Sequence[AddToComplexRequest], int]:
        apartment_alias = aliased(Apartment)

        stmt = (
            select(AddToComplexRequest)
            .where(apartment_alias.user_id == user_id)
            .options(
                orm.joinedload(AddToComplexRequest.floor)
                .joinedload(Floor.block)
                .joinedload(Block.complex),
                orm.joinedload(AddToComplexRequest.riser),
                orm.joinedload(
                    AddToComplexRequest.apartment.of_type(apartment_alias)
                ).joinedload(apartment_alias.user),
                orm.joinedload(
                    AddToComplexRequest.apartment.of_type(apartment_alias)
                ).selectinload(apartment_alias.gallery),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self.list_and_count(
            limit_offset,
            statement=stmt,
        )

        return results, total

    async def get_user_request(self, request_id: int) -> AddToComplexRequest:
        stmt = (
            select(AddToComplexRequest)
            .where(AddToComplexRequest.id == request_id)
            .options(
                orm.joinedload(AddToComplexRequest.floor),
                orm.joinedload(AddToComplexRequest.floor).joinedload(Floor.block),
                orm.joinedload(AddToComplexRequest.floor)
                .joinedload(Floor.block)
                .joinedload(Block.complex),
                orm.joinedload(AddToComplexRequest.riser),
                orm.joinedload(AddToComplexRequest.apartment),
                orm.joinedload(AddToComplexRequest.apartment).joinedload(
                    Apartment.user
                ),
                orm.joinedload(AddToComplexRequest.apartment).selectinload(
                    Apartment.gallery
                ),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

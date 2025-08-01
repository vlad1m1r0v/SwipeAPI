from typing import Sequence, Any

from sqlalchemy import select, func, Select
from sqlalchemy.orm import aliased, selectinload, joinedload

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from src.apartments.models import Apartment

from src.buildings.models import Block, Floor, Section, Riser

from src.builder.models import Complex, FavouriteComplex

from src.user.models import User


class FavouriteComplexRepository(SQLAlchemyAsyncRepository[FavouriteComplex]):
    model_type = FavouriteComplex

    async def get_favourite_complexes(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[FavouriteComplex], int]:
        block_alias = aliased(Block)
        floor_alias = aliased(Floor)
        apartment_alias = aliased(Apartment)

        min_price_subquery = (
            select(
                block_alias.complex_id.label("complex_id"),
                func.min(apartment_alias.price).label("min_price"),
            )
            .join(floor_alias, floor_alias.block_id == block_alias.id)
            .join(apartment_alias, apartment_alias.floor_id == floor_alias.id)
            .group_by(block_alias.complex_id)
            .subquery()
        )

        min_area_subquery = (
            select(
                block_alias.complex_id.label("complex_id"),
                func.min(apartment_alias.area).label("min_area"),
            )
            .join(floor_alias, floor_alias.block_id == block_alias.id)
            .join(apartment_alias, apartment_alias.floor_id == floor_alias.id)
            .group_by(block_alias.complex_id)
            .subquery()
        )

        stmt = (
            select(
                FavouriteComplex,
                min_price_subquery.c.min_price,
                min_area_subquery.c.min_area,
            )
            .join(FavouriteComplex.complex)
            .outerjoin(
                min_price_subquery, min_price_subquery.c.complex_id == Complex.id
            )
            .outerjoin(min_area_subquery, min_area_subquery.c.complex_id == Complex.id)
            .options(
                selectinload(FavouriteComplex.complex).selectinload(Complex.gallery),
            )
            .where(FavouriteComplex.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        favourites: list[FavouriteComplex] = []

        for fav, min_price, min_area in results:
            fav.complex.min_price = min_price
            fav.complex.min_area = min_area
            favourites.append(fav)

        return favourites, total

    async def get_favourite_complex_detail(self, favourite_id: int) -> FavouriteComplex:
        stmt = (
            select(FavouriteComplex)
            .where(FavouriteComplex.id == favourite_id)
            .options(
                # Favourite complex -> Complex
                joinedload(FavouriteComplex.complex),
                # Favourite complex -> Complex -> User
                joinedload(FavouriteComplex.complex).joinedload(Complex.user),
                # Favourite complex -> Complex -> User -> Contact
                joinedload(FavouriteComplex.complex)
                .joinedload(Complex.user)
                .joinedload(User.contact),
                # Favourite complex -> Complex -> Infrastructure
                joinedload(FavouriteComplex.complex).joinedload(Complex.infrastructure),
                # Favourite complex -> Complex -> Advantages
                joinedload(FavouriteComplex.complex).joinedload(Complex.advantages),
                # Favourite complex -> Complex -> Formalization and payments settings
                joinedload(FavouriteComplex.complex).joinedload(
                    Complex.formalization_and_payment_settings
                ),
                # Favourite complex -> Complex -> News
                joinedload(FavouriteComplex.complex).selectinload(Complex.news),
                # Favourite complex -> Complex -> Documents
                joinedload(FavouriteComplex.complex).selectinload(Complex.documents),
                # Favourite complex -> Complex -> Gallery
                joinedload(FavouriteComplex.complex).selectinload(Complex.gallery),
            )
        )

        result = await self.session.execute(stmt)
        fav: FavouriteComplex = result.scalar_one_or_none()

        building = fav.complex

        agg_stmt = (
            select(
                func.min(Apartment.price).label("min_price"),
                (func.sum(Apartment.price) / func.sum(Apartment.area)).label(
                    "avg_price_per_m2"
                ),
                func.min(Apartment.area).label("min_area"),
                func.max(Apartment.area).label("max_area"),
            )
            .join(Riser, Riser.id == Apartment.riser_id)
            .join(Section, Section.id == Riser.section_id)
            .join(Block, Block.id == Section.block_id)
            .join(Floor, Floor.id == Apartment.floor_id)
            .where(Block.complex_id == building.id)
        )

        result = await self.session.execute(agg_stmt)
        agg = result.first()

        building.min_price = agg.min_price
        building.avg_price_per_m2 = agg.avg_price_per_m2
        building.min_area = agg.min_area
        building.max_area = agg.max_area
        building.phone = building.user.contact.phone

        stmt = (
            select(
                Block.id, Block.no, func.count(Apartment.id).label("apartments_count")
            )
            .join(Section, Section.block_id == Block.id)
            .join(Riser, Riser.section_id == Section.id)
            .join(Apartment, Apartment.riser_id == Riser.id)
            .where(Block.complex_id == building.id)
            .group_by(Block.id)
            .order_by(Block.no)
        )

        result = await self.session.execute(stmt)
        building.apartments_per_block = result.all()

        return fav

    async def _custom_list_and_count(
        self,
        statement: Select,
        limit_offset: LimitOffset | None = None,
    ) -> tuple[Sequence[Any], int]:
        count_stmt = statement.with_only_columns(func.count())

        if limit_offset:
            statement = statement.limit(limit_offset.limit).offset(limit_offset.offset)

        result = await self.session.execute(statement)
        rows = result.all()

        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return rows, total

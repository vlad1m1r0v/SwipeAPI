from typing import Sequence, Any

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset, SearchFilter

from sqlalchemy import Select, func, select, orm
from sqlalchemy.orm import aliased, selectinload

from src.builder.models import Complex

from src.buildings.models import Block, Section, Floor, Riser

from src.apartments.models import Apartment

from src.user.models import User


class ComplexRepository(SQLAlchemyAsyncRepository[Complex]):
    model_type = Complex

    async def get_complexes_for_requests(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[Complex], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)
        search_filter = SearchFilter(
            field_name="name",
            value=search,
            ignore_case=True,
        )

        results, total = await self.list_and_count(
            limit_offset,
            search_filter,
        )

        return results, total

    async def get_complexes_for_feed_list(
        self, limit: int, offset: int
    ) -> tuple[Sequence[Complex], int]:
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
                Complex,
                min_price_subquery.c.min_price,
                min_area_subquery.c.min_area,
            )
            .outerjoin(
                min_price_subquery, min_price_subquery.c.complex_id == Complex.id
            )
            .outerjoin(min_area_subquery, min_area_subquery.c.complex_id == Complex.id)
            .options(selectinload(Complex.gallery))
            .limit(limit)
            .offset(offset)
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        complexes: list[Complex] = []

        for building, min_price, min_area in results:
            setattr(building, "min_price", min_price)
            setattr(building, "min_area", min_area)
            complexes.append(building)

        return complexes, total

    async def get_complex_detail(self, complex_id: int) -> Complex:
        stmt = (
            select(Complex)
            .where(Complex.id == complex_id)
            .options(
                orm.joinedload(Complex.infrastructure),
                orm.joinedload(Complex.advantages),
                orm.joinedload(Complex.formalization_and_payment_settings),
                orm.selectinload(Complex.news),
                orm.selectinload(Complex.documents),
                orm.selectinload(Complex.gallery),
                orm.joinedload(Complex.user).joinedload(User.contact),
            )
        )

        result = await self.session.execute(stmt)
        building: Complex = result.scalar_one_or_none()

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
            .where(Block.complex_id == building.id, Floor.block_id == Block.id)
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

        return building

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

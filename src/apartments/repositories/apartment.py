from typing import List, Sequence, Any

from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import select, func, and_, Select
from sqlalchemy.orm import joinedload, selectinload

from src.core.schemas import Base64Item, Action
from src.core.utils import convert_base64_to_starlette_file, save_file

from src.user.models import User

from src.apartments.models import Apartment, ApartmentGallery
from src.apartments.schemas import (
    CreateApartmentSchema,
    UpdateApartmentSchema,
)

from src.buildings.models import Block, Floor, Section, Riser


class ApartmentRepository(SQLAlchemyAsyncRepository[Apartment]):
    model_type = Apartment

    async def create_apartment(
        self, user_id: int, data: CreateApartmentSchema
    ) -> Apartment:
        fields = data.model_dump()

        scheme_base64 = fields.pop("scheme", "")
        scheme_starlette_file = convert_base64_to_starlette_file(scheme_base64)
        file_path = save_file(file=scheme_starlette_file)

        gallery: List[Base64Item] = fields.pop("gallery", [])

        instance: Apartment = await self.add(
            data=Apartment(**fields, user_id=user_id, scheme=file_path)
        )

        images_to_create: List[ApartmentGallery] = []

        for image in gallery:
            starlette_file = convert_base64_to_starlette_file(image.get("base64"))
            file_path = save_file(file=starlette_file)

            images_to_create.append(
                ApartmentGallery(
                    apartment_id=instance.id, photo=file_path, order=image.get("order")
                )
            )

        self.session.add_all(images_to_create)
        await self.session.commit()

        apartment = await self.get_apartment_detail_for_user(apartment_id=instance.id)
        return apartment

    async def update_apartment(
        self, item_id: int, data: UpdateApartmentSchema
    ) -> Apartment:
        fields = data.model_dump(exclude_none=True)

        if fields.get("scheme") is not None:
            scheme_base64 = fields.pop("scheme")
            scheme_starlette_file = convert_base64_to_starlette_file(scheme_base64)
            file_path = save_file(file=scheme_starlette_file)
            fields.setdefault("scheme", file_path)

        gallery: List[Base64Item] = fields.pop("gallery", [])

        apartment = await self.session.get(Apartment, item_id)

        for key, value in fields.items():
            setattr(apartment, key, value)

        images_to_add: List[ApartmentGallery] = []

        for image in gallery:
            if image.get("action") == Action.DELETED:
                image_to_delete = await self.session.get(
                    ApartmentGallery, image.get("id")
                )
                await self.session.delete(image_to_delete)

            if image.get("action") == Action.UPDATED:
                image_to_update = await self.session.get(
                    ApartmentGallery, image.get("id")
                )
                image_to_update.order = image.get("order")

            if image.get("action") == Action.CREATED:
                starlette_file = convert_base64_to_starlette_file(image.get("base64"))
                file_path = save_file(file=starlette_file)

                image_to_add = ApartmentGallery(
                    apartment_id=item_id,
                    photo=file_path,
                    order=image.get("order"),
                )
                images_to_add.append(image_to_add)

        self.session.add_all(images_to_add)
        await self.session.commit()

        apartment = await self.get_apartment_detail_for_user(apartment_id=item_id)
        return apartment

    async def get_apartment_detail_for_user(self, apartment_id: int) -> Apartment:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                Apartment,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(Apartment.id == apartment_id)
            .options(selectinload(Apartment.gallery))
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        apartment, floor_no, total_floors = row
        apartment.floor_no = floor_no
        apartment.total_floors = total_floors

        return apartment

    async def get_apartments_list_for_user(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[Sequence[Apartment], int]:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                Apartment,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(Apartment.user_id == user_id)
            .options(selectinload(Apartment.gallery))
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)
        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        apartments: list[Apartment] = []
        for apartment, floor_no, total_floors in results:
            apartment.floor_no = floor_no
            apartment.total_floors = total_floors
            apartments.append(apartment)

        return apartments, total

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
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                Apartment,
                (Apartment.price / Apartment.area).label("price_per_m2"),
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Floor, Apartment.floor_id == Floor.id)
            .join(Riser, Apartment.riser_id == Riser.id)
            .join(
                total_floors_subquery,
                Floor.block_id == total_floors_subquery.c.block_id,
            )
            .where(Riser.section_id == section_id)
        )

        filters = []

        if price_min is not None:
            filters.append(Apartment.price >= price_min)
        if price_max is not None:
            filters.append(Apartment.price <= price_max)

        if price_min_per_m2 is not None:
            filters.append((Apartment.price / Apartment.area) >= price_min_per_m2)
        if price_max_per_m2 is not None:
            filters.append((Apartment.price / Apartment.area) <= price_max_per_m2)

        if area_min is not None:
            filters.append(Apartment.area >= area_min)
        if area_max is not None:
            filters.append(Apartment.area <= area_max)

        if finishing is not None:
            filters.append(Apartment.finishing == finishing)

        if filters:
            stmt = stmt.where(and_(*filters))

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        apartments: list[Apartment] = []
        for apartment, price_per_m2, floor_no, total_floors in results:
            setattr(apartment, "price_per_m2", price_per_m2)
            setattr(apartment, "floor_no", floor_no)
            setattr(apartment, "total_floors", total_floors)
            apartments.append(apartment)

        return apartments, total

    async def get_apartment_detail_for_grid(self, apartment_id) -> Apartment:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                Apartment,
                (Apartment.price / Apartment.area).label("price_per_m2"),
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Floor, Apartment.floor_id == Floor.id)
            .join(Riser, Apartment.riser_id == Riser.id)
            .join(Section, Riser.section_id == Section.id)
            .join(Block, Section.block_id == Block.id)
            .join(
                total_floors_subquery,
                Floor.block_id == total_floors_subquery.c.block_id,
            )
            .options(
                joinedload(Apartment.riser)
                .joinedload(Riser.section)
                .joinedload(Section.block),
                joinedload(Apartment.floor),
                joinedload(Apartment.user).joinedload(User.contact),
            )
            .where(Apartment.id == apartment_id)
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        apartment, price_per_m2, floor_no, total_floors = row
        apartment.price_per_m2 = price_per_m2
        apartment.floor_no = floor_no
        apartment.total_floors = total_floors
        apartment.section = apartment.riser.section
        apartment.block = apartment.riser.section.block
        apartment.contact = apartment.user.contact

        return apartment

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

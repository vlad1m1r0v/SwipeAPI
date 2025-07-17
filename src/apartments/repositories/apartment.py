from typing import List, Sequence

from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import orm, select

from src.builder.models import Section
from src.core.schemas import Base64Item, Action
from src.core.utils import (
    convert_base64_to_starlette_file,
    save_file,
)

from src.builder.models import Riser, Block

from src.apartments.models import Apartment, ApartmentGallery
from src.apartments.schemas import CreateApartmentSchema, UpdateApartmentSchema


class ApartmentRepository(SQLAlchemyAsyncRepository[Apartment]):
    model_type = Apartment

    async def get_apartment_details(self, apartment_id: int) -> Apartment:
        stmt = (
            select(Apartment)
            .where(Apartment.id == apartment_id)
            .options(
                orm.joinedload(Apartment.floor),
                orm.joinedload(Apartment.riser),
                orm.joinedload(Apartment.riser).joinedload(Riser.section),
                orm.joinedload(Apartment.riser)
                .joinedload(Riser.section)
                .joinedload(Section.block),
                orm.joinedload(Apartment.riser)
                .joinedload(Riser.section)
                .joinedload(Section.block)
                .joinedload(Block.complex),
                orm.selectinload(Apartment.gallery),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_apartments(
        self, limit: int, offset: int, user_id: int
    ) -> tuple[Sequence[Apartment], int]:
        stmt = (
            select(Apartment)
            .where(Apartment.user_id == user_id)
            .options(
                orm.joinedload(Apartment.floor),
                orm.joinedload(Apartment.riser),
                orm.joinedload(Apartment.riser).joinedload(Riser.section),
                orm.joinedload(Apartment.riser)
                .joinedload(Riser.section)
                .joinedload(Section.block),
                orm.joinedload(Apartment.riser)
                .joinedload(Riser.section)
                .joinedload(Section.block)
                .joinedload(Block.complex),
                orm.selectinload(Apartment.gallery),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)

        results, total = await self.list_and_count(
            limit_offset,
            statement=stmt,
        )

        return results, total

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

        apartment = await self.get_apartment_details(apartment_id=instance.id)
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

        apartment = await self.get_apartment_details(apartment_id=item_id)
        return apartment

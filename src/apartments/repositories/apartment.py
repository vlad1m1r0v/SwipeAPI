from typing import List

from fastapi import Request

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import orm, select

from src.builder.models import Section
from src.core.schemas import Base64Item
from src.core.utils import (
    convert_base64_to_starlette_file,
    save_file,
)

from src.builder.models import Riser

from src.apartments.models import Apartment, ApartmentGallery
from src.apartments.schemas import CreateApartmentSchema


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
                orm.selectinload(Apartment.gallery),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_apartment_item(self, apartment_id: int) -> Apartment: ...

    async def create_apartment(
        self, request: Request, user_id: int, data: CreateApartmentSchema
    ) -> Apartment:
        fields = data.model_dump()

        scheme_base64 = fields.pop("scheme", "")
        scheme_starlette_file = convert_base64_to_starlette_file(scheme_base64)
        scheme_file_info = save_file(request=request, file=scheme_starlette_file)

        gallery: List[Base64Item] = fields.pop("gallery", [])

        instance: Apartment = await self.add(
            data=Apartment(
                **fields, user_id=user_id, scheme=scheme_file_info.model_dump()
            )
        )

        images_to_create: List[ApartmentGallery] = []

        for image in gallery:
            starlette_file = convert_base64_to_starlette_file(image.get("base64"))
            file_info = save_file(request=request, file=starlette_file)

            images_to_create.append(
                ApartmentGallery(
                    apartment_id=instance.id,
                    photo=file_info.model_dump(),
                    order=image.get("order"),
                )
            )

        self.session.add_all(images_to_create)
        await self.session.commit()

        apartment = await self.get_apartment_details(apartment_id=instance.id)
        return apartment

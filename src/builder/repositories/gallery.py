from typing import List, Sequence

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select

from src.core.schemas import Base64Item, Action, GetGalleryImageSchema
from src.core.utils import save_file, convert_base64_to_starlette_file

from src.builder.models import ComplexGallery


class GalleryRepository(SQLAlchemyAsyncRepository[ComplexGallery]):
    model_type = ComplexGallery

    async def update_gallery(
        self,
        complex_id: int,
        media_set: List[Base64Item],
    ) -> List[GetGalleryImageSchema]:
        for image in media_set:
            if image.action == Action.DELETED:
                await self.delete(item_id=image.id)

            if image.action == Action.UPDATED:
                await self.update(data=image.model_dump(exclude={"action", "base64"}))

            images_to_add = []

            if image.action == Action.CREATED:
                starlette_file = convert_base64_to_starlette_file(image.base64)
                file_path = save_file(file=starlette_file)

                image_to_add = ComplexGallery(
                    complex_id=complex_id,
                    photo=file_path,
                    order=image.order,
                )
                images_to_add.append(image_to_add)

            await self.add_many(images_to_add)
            await self.session.commit()

        stmt = (
            select(ComplexGallery)
            .where(ComplexGallery.complex_id == complex_id)
            .order_by(ComplexGallery.order)
        )

        fetched_gallery: Sequence[ComplexGallery] = await self.list(statement=stmt)

        return [
            GetGalleryImageSchema(id=item.id, photo=item.photo)
            for item in fetched_gallery
        ]

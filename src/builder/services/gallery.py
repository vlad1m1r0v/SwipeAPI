from typing import List

from fastapi import Request

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.core.schemas import Base64Item, Action
from src.core.utils import save_file, convert_base64_to_starlette_file

from src.builder.models import ComplexGallery
from src.builder.repositories import GalleryRepository


class GalleryService(
    SQLAlchemyAsyncRepositoryService[ComplexGallery, GalleryRepository]
):
    repository_type = GalleryRepository

    async def update_gallery(
        self,
        complex_id: int,
        request: Request,
        media_set: List[Base64Item],
    ) -> None:
        for image in media_set:
            if image.action == Action.DELETED:
                await self.delete(item_id=image.id)

            if image.action == Action.UPDATED:
                await self.update(item_id=image.id, data={"order": image.order})

            if image.action == Action.CREATED:
                starlette_file = convert_base64_to_starlette_file(image.base64)

                file_info = save_file(request=request, file=starlette_file)
                await self.create(
                    data={
                        "complex_id": complex_id,
                        "photo": file_info.model_dump(),
                        "order": image.order,
                    }
                )

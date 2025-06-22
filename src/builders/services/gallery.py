from typing import List

import io

import base64

from fastapi import Request
from starlette.datastructures import UploadFile

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.core.schemas import MediaItem, Action
from src.core.utils import save_file

from src.builders.models import ComplexGallery
from src.builders.repositories import GalleryRepository


class GalleryService(
    SQLAlchemyAsyncRepositoryService[ComplexGallery, GalleryRepository]
):
    repository_type = GalleryRepository

    async def update_gallery(
        self,
        complex_id: int,
        request: Request,
        media_set: List[MediaItem],
    ) -> None:
        for image in media_set:
            if image.action == Action.DELETED:
                await self.delete(item_id=image.id)

            if image.action == Action.UPDATED:
                await self.update(item_id=image.id, data={"order": image.order})

            if image.action == Action.CREATED:
                base64_str = image.base64.split(",")[1]
                decoded = base64.b64decode(base64_str)

                file = io.BytesIO(decoded)
                file.seek(0)

                starlette_file = UploadFile(file=file, filename="image.png")

                file_info = save_file(request=request, file=starlette_file)
                await self.create(
                    data={
                        "complex_id": complex_id,
                        "photo": file_info.model_dump(),
                        "order": image.order,
                    }
                )

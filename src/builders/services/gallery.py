from typing import List

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import ComplexGallery
from src.builders.repositories import GalleryRepository
from src.builders.schemas import CreateGalleryImageSchema


class GalleryService(
    SQLAlchemyAsyncRepositoryService[ComplexGallery, GalleryRepository]
):
    repository_type = GalleryRepository

    async def update_gallery(
        self, complex_id: int, images: List[CreateGalleryImageSchema]
    ) -> None:
        old_images = await self.list(complex_id=complex_id)

        for image in old_images:
            await self.repository.delete(image.id)

        instances = []

        for image in images:
            instances.append(await self.to_model(image))

        await self.repository.add_many(data=instances)

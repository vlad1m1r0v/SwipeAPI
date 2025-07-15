from typing import List

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.core.schemas import Base64Item, GetGalleryImageSchema

from src.builder.models import ComplexGallery
from src.builder.repositories import GalleryRepository


class GalleryService(
    SQLAlchemyAsyncRepositoryService[ComplexGallery, GalleryRepository]
):
    repository_type = GalleryRepository

    async def update_gallery(
        self,
        complex_id: int,
        media_set: List[Base64Item],
    ) -> List[GetGalleryImageSchema]:
        return await self.repository.update_gallery(complex_id, media_set)

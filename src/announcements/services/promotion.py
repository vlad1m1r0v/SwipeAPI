from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Promotion
from src.announcements.repositories import AnnouncementPromotionRepository


class AnnouncementPromotionService(
    SQLAlchemyAsyncRepositoryService[Promotion, AnnouncementPromotionRepository]
):
    repository_type = AnnouncementPromotionRepository

    async def update_promotion(self, promotion_id: int, data: dict) -> Promotion:
        return await self.repository.update_promotion(promotion_id, data)

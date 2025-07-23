from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Promotion
from src.announcements.repositories import AnnouncementPromotionRepository


class AnnouncementPromotionService(
    SQLAlchemyAsyncRepositoryService[Promotion, AnnouncementPromotionRepository]
):
    repository_type = AnnouncementPromotionRepository

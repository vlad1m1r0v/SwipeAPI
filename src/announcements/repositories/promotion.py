from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import Promotion


class AnnouncementPromotionRepository(SQLAlchemyAsyncRepository[Promotion]):
    model_type = Promotion

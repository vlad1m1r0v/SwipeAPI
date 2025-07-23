from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import AnnouncementView


class AnnouncementViewRepository(SQLAlchemyAsyncRepository[AnnouncementView]):
    model_type = AnnouncementView

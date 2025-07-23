from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import Filter


class AnnouncementFilterRepository(SQLAlchemyAsyncRepository[Filter]):
    model_type = Filter

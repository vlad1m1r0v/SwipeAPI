from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.user.models import NotificationSettings


class NotificationSettingsRepository(SQLAlchemyAsyncRepository[NotificationSettings]):
    model_type = NotificationSettings

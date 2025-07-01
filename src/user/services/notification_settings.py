from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import NotificationSettings
from src.user.repositories import NotificationSettingsRepository


class NotificationSettingsService(
    SQLAlchemyAsyncRepositoryService[
        NotificationSettings, NotificationSettingsRepository
    ]
):
    repository_type = NotificationSettingsRepository

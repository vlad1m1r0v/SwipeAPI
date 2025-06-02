from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.models import NotificationSettings
from src.users.repositories import NotificationSettingsRepository


class NotificationSettingsService(
    SQLAlchemyAsyncRepositoryService[
        NotificationSettings, NotificationSettingsRepository
    ]
):
    repository_type = NotificationSettingsRepository

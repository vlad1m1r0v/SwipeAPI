from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import FormalizationAndPaymentSettings
from src.builders.repositories import FormalizationAndPaymentSettingsRepository


class FormalizationAndPaymentSettingsService(
    SQLAlchemyAsyncRepositoryService[
        FormalizationAndPaymentSettings, FormalizationAndPaymentSettingsRepository
    ]
):
    repository_type = FormalizationAndPaymentSettingsRepository

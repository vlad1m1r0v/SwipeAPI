from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import FormalizationAndPaymentSettings
from src.builder.repositories import FormalizationAndPaymentSettingsRepository


class FormalizationAndPaymentSettingsService(
    SQLAlchemyAsyncRepositoryService[
        FormalizationAndPaymentSettings, FormalizationAndPaymentSettingsRepository
    ]
):
    repository_type = FormalizationAndPaymentSettingsRepository

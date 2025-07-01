from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import FormalizationAndPaymentSettings


class FormalizationAndPaymentSettingsRepository(
    SQLAlchemyAsyncRepository[FormalizationAndPaymentSettings]
):
    model_type = FormalizationAndPaymentSettings

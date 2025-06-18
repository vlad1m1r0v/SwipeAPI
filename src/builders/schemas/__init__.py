from .formalization_and_payment_settings import (
    GetFormalizationAndPaymentSettingsSchema,
    UpdateFormalizationAndPaymentSettingsSchema,
)

from .advantages import GetAdvantagesSchema, UpdateAdvantagesSchema

from .infrastructure import GetInfrastructureSchema, UpdateInfrastructureSchema

from .complex import GetComplexSchema, UpdateComplexSchema, GetBuilderSchema

from .news import GetNewsSchema, CreateNewsSchema, UpdateNewsSchema

from .document import GetDocumentSchema, CreateDocumentSchema, UpdateDocumentSchema

__all__ = [
    "GetFormalizationAndPaymentSettingsSchema",
    "UpdateFormalizationAndPaymentSettingsSchema",
    "GetAdvantagesSchema",
    "UpdateAdvantagesSchema",
    "GetInfrastructureSchema",
    "UpdateInfrastructureSchema",
    "GetComplexSchema",
    "UpdateComplexSchema",
    "GetBuilderSchema",
    "GetNewsSchema",
    "CreateNewsSchema",
    "UpdateNewsSchema",
    "GetDocumentSchema",
    "CreateDocumentSchema",
    "UpdateDocumentSchema",
]

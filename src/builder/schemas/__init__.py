from .formalization_and_payment_settings import (
    GetFormalizationAndPaymentSettingsSchema,
    UpdateFormalizationAndPaymentSettingsSchema,
)

from .advantages import (
    GetAdvantagesSchema,
    UpdateAdvantagesSchema,
)

from .infrastructure import (
    GetInfrastructureSchema,
    UpdateInfrastructureSchema,
)

from .complex import (
    GetComplexSchema,
    UpdateComplexSchema,
    GetBuilderSchema,
    GetComplexFeedListItemSchema,
    GetComplexFeedDetailSchema,
)

from .news import GetNewsSchema, CreateNewsSchema, UpdateNewsSchema

from .document import GetDocumentSchema, CreateDocumentSchema, UpdateDocumentSchema

from .favourite import (
    CreateFavouriteComplexSchema,
    GetFavouriteComplexListItemSchema,
    GetFavouriteComplexDetailSchema,
)

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
    "GetComplexFeedListItemSchema",
    "GetComplexFeedDetailSchema",
    "GetNewsSchema",
    "CreateNewsSchema",
    "UpdateNewsSchema",
    "GetDocumentSchema",
    "CreateDocumentSchema",
    "UpdateDocumentSchema",
    "CreateFavouriteComplexSchema",
    "GetFavouriteComplexListItemSchema",
    "GetFavouriteComplexDetailSchema",
]

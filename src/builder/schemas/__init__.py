from .formalization_and_payment_settings import (
    GetFormalizationAndPaymentSettingsSchema,
    UpdateFormalizationAndPaymentSettingsSchema,
)

from .advantages import GetAdvantagesSchema, UpdateAdvantagesSchema

from .infrastructure import GetInfrastructureSchema, UpdateInfrastructureSchema

from .complex import GetComplexSchema, UpdateComplexSchema, GetBuilderSchema

from .news import GetNewsSchema, CreateNewsSchema, UpdateNewsSchema

from .document import GetDocumentSchema, CreateDocumentSchema, UpdateDocumentSchema

from .block import GetBlockSchema, CreateBlockSchema, UpdateBlockSchema

from .section import GetSectionSchema, CreateSectionSchema, UpdateSectionSchema

from .floor import GetFloorSchema, CreateFloorSchema, UpdateFloorSchema

from .riser import GetRiserSchema, CreateRiserSchema, UpdateRiserSchema

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
    "GetBlockSchema",
    "CreateBlockSchema",
    "UpdateBlockSchema",
    "GetSectionSchema",
    "CreateSectionSchema",
    "UpdateSectionSchema",
    "GetFloorSchema",
    "CreateFloorSchema",
    "UpdateFloorSchema",
    "GetRiserSchema",
    "CreateRiserSchema",
    "UpdateRiserSchema",
]

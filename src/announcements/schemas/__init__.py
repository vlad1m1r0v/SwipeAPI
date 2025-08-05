from .announcement import CreateAnnouncementSchema

from .promotion import CreatePromotionSchema
from .view import CreateViewSchema
from .favourite import CreateFavouriteAnnouncementSchema
from .filter import CreateFilterSchema
from .complaint import CreateComplaintSchema

__all__ = [
    "CreateAnnouncementSchema",
    "CreatePromotionSchema",
    "CreateViewSchema",
    "CreateFavouriteAnnouncementSchema",
    "CreateFilterSchema",
    "CreateComplaintSchema",
]

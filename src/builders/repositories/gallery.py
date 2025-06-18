from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import ComplexGallery


class GalleryRepository(SQLAlchemyAsyncRepository[ComplexGallery]):
    model_type = ComplexGallery

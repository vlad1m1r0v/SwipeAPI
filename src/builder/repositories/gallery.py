from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import ComplexGallery


class GalleryRepository(SQLAlchemyAsyncRepository[ComplexGallery]):
    model_type = ComplexGallery

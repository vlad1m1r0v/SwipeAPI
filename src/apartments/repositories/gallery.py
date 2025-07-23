from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.apartments.models import ApartmentGallery


class ApartmentGalleryRepository(SQLAlchemyAsyncRepository[ApartmentGallery]):
    model_type = ApartmentGallery

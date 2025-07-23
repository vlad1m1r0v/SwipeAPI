from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.apartments.models import ApartmentGallery
from src.apartments.repositories import ApartmentGalleryRepository


class ApartmentGalleryService(
    SQLAlchemyAsyncRepositoryService[ApartmentGallery, ApartmentGalleryRepository]
):
    repository_type = ApartmentGalleryRepository

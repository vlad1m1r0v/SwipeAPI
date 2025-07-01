from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Advantages
from src.builder.repositories import AdvantagesRepository


class AdvantagesService(
    SQLAlchemyAsyncRepositoryService[Advantages, AdvantagesRepository]
):
    repository_type = AdvantagesRepository

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Advantages
from src.builders.repositories import AdvantagesRepository


class AdvantagesService(
    SQLAlchemyAsyncRepositoryService[Advantages, AdvantagesRepository]
):
    repository_type = AdvantagesRepository

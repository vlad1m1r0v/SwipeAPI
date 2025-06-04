from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Infrastructure
from src.builders.repositories import InfrastructureRepository


class InfrastructureService(
    SQLAlchemyAsyncRepositoryService[Infrastructure, InfrastructureRepository]
):
    repository_type = InfrastructureRepository

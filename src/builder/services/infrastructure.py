from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Infrastructure
from src.builder.repositories import InfrastructureRepository


class InfrastructureService(
    SQLAlchemyAsyncRepositoryService[Infrastructure, InfrastructureRepository]
):
    repository_type = InfrastructureRepository

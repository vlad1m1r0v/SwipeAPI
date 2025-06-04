from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Complex
from src.builders.repositories import ComplexRepository


class ComplexService(SQLAlchemyAsyncRepositoryService[Complex, ComplexRepository]):
    repository_type = ComplexRepository

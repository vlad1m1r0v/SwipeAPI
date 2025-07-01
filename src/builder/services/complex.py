from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Complex
from src.builder.repositories import ComplexRepository


class ComplexService(SQLAlchemyAsyncRepositoryService[Complex, ComplexRepository]):
    repository_type = ComplexRepository

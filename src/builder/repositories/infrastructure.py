from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Infrastructure


class InfrastructureRepository(SQLAlchemyAsyncRepository[Infrastructure]):
    model_type = Infrastructure

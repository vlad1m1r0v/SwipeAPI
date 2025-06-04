from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import Infrastructure


class InfrastructureRepository(SQLAlchemyAsyncRepository[Infrastructure]):
    model_type = Infrastructure

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import Complex


class ComplexRepository(SQLAlchemyAsyncRepository[Complex]):
    model_type = Complex

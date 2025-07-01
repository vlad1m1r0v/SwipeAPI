from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Complex


class ComplexRepository(SQLAlchemyAsyncRepository[Complex]):
    model_type = Complex

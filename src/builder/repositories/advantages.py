from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Advantages


class AdvantagesRepository(SQLAlchemyAsyncRepository[Advantages]):
    model_type = Advantages

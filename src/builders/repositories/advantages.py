from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builders.models import Advantages


class AdvantagesRepository(SQLAlchemyAsyncRepository[Advantages]):
    model_type = Advantages

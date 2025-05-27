from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.admins.models import Blacklist


class BlacklistRepository(SQLAlchemyAsyncRepository[Blacklist]):
    model_type = Blacklist


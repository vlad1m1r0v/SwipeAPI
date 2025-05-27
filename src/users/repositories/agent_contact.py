from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.users.models import AgentContact


class AgentContactRepository(SQLAlchemyAsyncRepository[AgentContact]):
    model_type = AgentContact

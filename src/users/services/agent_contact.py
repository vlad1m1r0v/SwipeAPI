from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.models import AgentContact
from src.users.repositories import AgentContactRepository


class AgentContactService(SQLAlchemyAsyncRepositoryService[AgentContact, AgentContactRepository]):
    repository_type = AgentContactRepository

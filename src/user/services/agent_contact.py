from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import AgentContact
from src.user.repositories import AgentContactRepository


class AgentContactService(
    SQLAlchemyAsyncRepositoryService[AgentContact, AgentContactRepository]
):
    repository_type = AgentContactRepository

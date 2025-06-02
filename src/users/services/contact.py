from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.models import Contact
from src.users.repositories import ContactRepository


class ContactService(SQLAlchemyAsyncRepositoryService[Contact, ContactRepository]):
    repository_type = ContactRepository

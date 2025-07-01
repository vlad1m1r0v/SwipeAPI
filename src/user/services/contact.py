from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import Contact
from src.user.repositories import ContactRepository


class ContactService(SQLAlchemyAsyncRepositoryService[Contact, ContactRepository]):
    repository_type = ContactRepository

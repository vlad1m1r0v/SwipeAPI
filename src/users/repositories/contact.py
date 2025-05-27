from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.users.models import Contact


class ContactRepository(SQLAlchemyAsyncRepository[Contact]):
    model_type = Contact
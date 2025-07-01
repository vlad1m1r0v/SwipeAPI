from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import Document


class DocumentRepository(SQLAlchemyAsyncRepository[Document]):
    model_type = Document

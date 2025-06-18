from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import Document
from src.builders.repositories import DocumentRepository


class DocumentService(SQLAlchemyAsyncRepositoryService[Document, DocumentRepository]):
    repository_type = DocumentRepository

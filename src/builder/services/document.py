from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import Document
from src.builder.repositories import DocumentRepository


class DocumentService(SQLAlchemyAsyncRepositoryService[Document, DocumentRepository]):
    repository_type = DocumentRepository

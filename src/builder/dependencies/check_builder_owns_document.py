from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.builder.services import DocumentService

from src.auth.dependencies import builder_from_token

from src.builder.schemas import GetBuilderSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_document(
    document_id: int,
    document_service: FromDishka[DocumentService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    document = await document_service.get(item_id=document_id)

    if document.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder

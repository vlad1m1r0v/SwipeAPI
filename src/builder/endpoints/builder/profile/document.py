from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from src.core.utils import save_file, generate_examples
from src.core.schemas import SuccessResponse
from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)

from src.auth.dependencies import builder_from_token

from src.builder.services import DocumentService
from src.builder.dependencies import check_builder_owns_document
from src.builder.schemas import (
    GetBuilderSchema,
    GetDocumentSchema,
    CreateDocumentSchema,
    UpdateDocumentSchema,
)

router = APIRouter(prefix="/documents")


@router.post(
    path="",
    response_model=SuccessResponse[GetDocumentSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
@inject
async def create_document(
    document_service: FromDishka[DocumentService],
    name: str = Form(),
    file: UploadFile = File(),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetDocumentSchema]:
    fields = CreateDocumentSchema(name=name, file=save_file(file=file))
    document = await document_service.create(
        {"complex_id": builder.complex.id, **fields.model_dump()}
    )
    return SuccessResponse(
        data=document_service.to_schema(data=document, schema_type=GetDocumentSchema)
    )


@router.patch(
    path="/{document_id}",
    response_model=SuccessResponse[GetDocumentSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def update_document(
    document_id: int,
    document_service: FromDishka[DocumentService],
    name: Optional[str] = Form(default=None),
    file: Optional[UploadFile] = File(default=None),
    _: GetBuilderSchema = Depends(check_builder_owns_document),
) -> SuccessResponse[GetDocumentSchema]:
    fields = UpdateDocumentSchema(
        name=name,
        file=save_file(file=file) if file else None,
    )
    document = await document_service.update(
        data=fields.model_dump(exclude_none=True), item_id=document_id
    )
    return SuccessResponse(
        data=document_service.to_schema(data=document, schema_type=GetDocumentSchema)
    )


@router.delete(
    path="/{document_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def delete_document(
    document_id: int,
    document_service: FromDishka[DocumentService],
    _: GetBuilderSchema = Depends(check_builder_owns_document),
) -> SuccessResponse:
    await document_service.delete(item_id=document_id)
    return SuccessResponse(message="Document has been deleted successfully.")

from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File

from src.core.utils import save_file

from src.users.services import UserService

from src.auth.dependencies import builder_from_token

from src.builders.services import DocumentService
from src.builders.dependencies import check_builder_owns_document
from src.builders.schemas import (
    GetBuilderSchema,
    CreateDocumentSchema,
    UpdateDocumentSchema,
)

router = APIRouter(prefix="/documents")


@router.post("", response_model=GetBuilderSchema)
@inject
async def create_document(
    request: Request,
    document_service: FromDishka[DocumentService],
    user_service: FromDishka[UserService],
    name: str = Form(),
    file: UploadFile = File(),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    fields = CreateDocumentSchema(name=name, file=save_file(file=file, request=request))

    await document_service.create(
        {"complex_id": builder.complex.id, **fields.model_dump()}
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)


@router.patch("/{document_id}", response_model=GetBuilderSchema)
@inject
async def update_document(
    request: Request,
    document_id: int,
    document_service: FromDishka[DocumentService],
    user_service: FromDishka[UserService],
    name: Optional[str] = Form(default=None),
    file: Optional[UploadFile] = File(default=None),
    builder: GetBuilderSchema = Depends(check_builder_owns_document),
) -> GetBuilderSchema:
    fields = UpdateDocumentSchema(
        name=name,
        file=save_file(file=file, request=request) if file else None,
    )

    await document_service.update(
        data=fields.model_dump(exclude_none=True), item_id=document_id
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)


@router.delete("/{document_id}", response_model=GetBuilderSchema)
@inject
async def delete_document(
    document_id: int,
    document_service: FromDishka[DocumentService],
    user_service: FromDishka[UserService],
    builder: GetBuilderSchema = Depends(check_builder_owns_document),
) -> GetBuilderSchema:
    await document_service.delete(item_id=document_id)
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)

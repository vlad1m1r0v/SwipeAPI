from typing import Optional

from pydantic import EmailStr

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form, UploadFile, File, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessResponse
from src.core.utils import save_file, generate_examples
from src.core.exceptions import (
    DuplicateKeyException,
    IntegrityErrorException,
    NotFoundException,
)

from src.auth.dependencies import admin_from_token, payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.admin.services import NotaryService
from src.admin.schemas import (
    GetNotarySchema,
    CreateNotarySchema,
    UpdateNotarySchema,
    GetAdminSchema,
)

router = APIRouter(prefix="/notaries", tags=["Admin: Notaries"])
notaries = APIRouter(prefix="/notaries", tags=["Notaries"])


@notaries.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetNotarySchema]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_notaries(
    notary_service: FromDishka[NotaryService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetNotarySchema]]:
    results, total = await notary_service.get_notaries(limit, offset, search)
    return SuccessResponse(
        data=notary_service.to_schema(
            data=results, total=total, schema_type=GetNotarySchema
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[GetNotarySchema],
    responses=generate_examples(
        IntegrityErrorException, DuplicateKeyException, auth=True, role=True
    ),
)
@inject
async def create_notary(
    notary_service: FromDishka[NotaryService],
    _: GetAdminSchema = Depends(admin_from_token),
    first_name: str = Form(),
    last_name: str = Form(),
    email: EmailStr = Form(),
    phone: str = Form(),
    photo: UploadFile = File(),
) -> SuccessResponse[GetNotarySchema]:
    fields = CreateNotarySchema(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        photo=save_file(file=photo),
    )

    notary = await notary_service.create(data={**fields.model_dump()})
    return SuccessResponse(
        data=notary_service.to_schema(data=notary, schema_type=GetNotarySchema)
    )


@router.patch(
    path="/{notary_id}",
    response_model=SuccessResponse[GetNotarySchema],
    responses=generate_examples(
        IntegrityErrorException, DuplicateKeyException, auth=True, role=True
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_notary(
    notary_id: int,
    notary_service: FromDishka[NotaryService],
    _: GetAdminSchema = Depends(admin_from_token),
    first_name: Optional[str] = Form(default=None),
    last_name: Optional[str] = Form(default=None),
    email: Optional[EmailStr] = Form(default=None),
    phone: Optional[str] = Form(default=None),
    photo: Optional[UploadFile] = File(default=None),
) -> SuccessResponse[GetNotarySchema]:
    fields = UpdateNotarySchema(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        photo=save_file(file=photo) if photo else None,
    )

    notary = await notary_service.update(
        item_id=notary_id, data={**fields.model_dump(exclude_none=True)}
    )
    return SuccessResponse(
        data=notary_service.to_schema(data=notary, schema_type=GetNotarySchema)
    )


@router.delete(
    path="/{notary_id}",
    response_model=SuccessResponse,
    responses=generate_examples(NotFoundException, auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_notary(
    notary_service: FromDishka[NotaryService],
    notary_id: int,
    _: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse:
    await notary_service.delete(item_id=notary_id)
    return SuccessResponse(
        message="Notary deleted successfully.",
    )

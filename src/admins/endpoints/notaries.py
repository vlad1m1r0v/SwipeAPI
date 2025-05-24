from typing import (
    Optional
)

from pydantic import EmailStr

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form,
    UploadFile,
    File,
    Query
)

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessfulMessageSchema
from src.core.utils import (
    save_file,
    delete_file
)

from src.auth.dependencies import admin_from_token

from src.admins.services import (
    NotaryService
)
from src.admins.schemas import (
    GetNotarySchema,
    CreateNotarySchema,
    UpdateNotarySchema,
    GetAdminSchema
)

router = APIRouter(prefix="/notaries")


@router.get("", response_model=OffsetPagination[GetNotarySchema])
@inject
async def get_notaries(
        notary_service: FromDishka[NotaryService],
        limit: int = Query(default=20),
        offset: int = Query(default=0),
        search: str = Query(default=""),
        _: GetAdminSchema = Depends(admin_from_token),
) -> OffsetPagination[GetNotarySchema]:
    results, total = await notary_service.get_notaries(limit, offset, search)
    return notary_service.to_schema(data=results, total=total, schema_type=GetNotarySchema)


@router.post("", response_model=GetNotarySchema)
@inject
async def create_notary(
        request: Request,
        notary_service: FromDishka[NotaryService],
        _: GetAdminSchema = Depends(admin_from_token),
        first_name: str = Form(),
        last_name: str = Form(),
        email: EmailStr = Form(),
        phone: str = Form(),
        photo: UploadFile = File(),
) -> GetNotarySchema:
    fields = CreateNotarySchema(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        photo=save_file(request=request, file=photo),
    )

    notary = await notary_service.create(data={**fields.model_dump()})
    return notary_service.to_schema(data=notary, schema_type=GetNotarySchema)


@router.patch("/{notary_id}", response_model=GetNotarySchema)
@inject
async def update_notary(
        request: Request,
        notary_id: int,
        notary_service: FromDishka[NotaryService],
        _: GetAdminSchema = Depends(admin_from_token),
        first_name: Optional[str] = Form(default=None),
        last_name: Optional[str] = Form(default=None),
        email: Optional[EmailStr] = Form(default=None),
        phone: Optional[str] = Form(default=None),
        photo: Optional[UploadFile] = File(default=None),
) -> GetNotarySchema:
    notary_from_db = await notary_service.get(item_id=notary_id)

    if notary_from_db.photo is not None:
        delete_file(notary_from_db.photo['content_path'])

    fields = UpdateNotarySchema(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        photo=save_file(request=request, file=photo)
    )

    notary = await notary_service.update(item_id=notary_id, data={**fields.model_dump(exclude_none=True)})
    return notary_service.to_schema(data=notary, schema_type=GetNotarySchema)


@router.delete("/{notary_id}", response_model=SuccessfulMessageSchema)
@inject
async def delete_notary(
        notary_service: FromDishka[NotaryService],
        notary_id: int,
        _: GetAdminSchema = Depends(admin_from_token),
):
    record = await notary_service.delete(item_id=notary_id)
    delete_file(record.photo['content_path'])

    return SuccessfulMessageSchema(
        message="Notary has been deleted.",
    )

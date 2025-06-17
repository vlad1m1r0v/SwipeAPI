from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File

from src.core.utils import save_file

from src.auth.dependencies import user_from_token

from src.users.services import UserService
from src.users.schemas import GetUserSchema, UpdateUserAccountSchema

router = APIRouter()


@router.patch("/account")
@inject
async def update_account(
    request: Request,
    user_service: FromDishka[UserService],
    email: Optional[str] = Form(default=None),
    name: Optional[str] = Form(default=None),
    phone: Optional[str] = Form(default=None),
    photo: Optional[UploadFile] = File(default=None),
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    fields = UpdateUserAccountSchema(
        email=email,
        name=name,
        phone=phone,
        photo=save_file(file=photo, request=request) if photo else None,
    )

    await user_service.update(
        data={**fields.model_dump(exclude_none=True)}, item_id=user.id
    )

    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)

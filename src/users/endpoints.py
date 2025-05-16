from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import (
    APIRouter,
    Depends, UploadFile
)

from advanced_alchemy.types import FileObject

from src.auth.dependencies import user_from_token

from src.users.services import UserService
from src.users.dependencies import update_user_form
from src.users.schemas import (
    UpdateUserSchema,
    GetUserSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/account")
@inject
async def update_account(
    user_service: FromDishka[UserService],
    user: GetUserSchema = Depends(user_from_token),
    data: tuple[UpdateUserSchema, Optional[UploadFile]] = Depends(update_user_form),
) -> GetUserSchema:
    fields, photo = data

    updated_data = fields.model_dump(exclude_none=True)

    if photo:
        file_obj = FileObject(
            backend='local',
            filename=photo.filename,
            content_type=photo.content_type,
            content=await photo.read(),
        )

        file_obj.save()

        updated_data['photo'] = file_obj

    user = await user_service.update(
        data=updated_data,
        item_id=user.id
    )
    return user_service.to_schema(data=user, schema_type=GetUserSchema)

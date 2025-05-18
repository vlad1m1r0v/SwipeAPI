from typing import (
    Optional,
    Annotated
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File
)

from src.core.schemas import SuccessfulMessageSchema

from src.auth.dependencies import user_from_token
from src.auth.schemas import (
    UpdatePasswordSchema
)

from src.users.services import UserService
from src.users.schemas import (
    UpdateUserSchema,
    GetUserSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/account")
@inject
async def update_account(
        user_service: FromDishka[UserService],
        email: Optional[str] = Form(default=None),
        name: Optional[str] = Form(default=None),
        phone: Optional[str] = Form(default=None),
        photo: Optional[UploadFile] = File(default=None),
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    fields = UpdateUserSchema(
        email=email,
        name=name,
        phone=phone
    )

    data = {**fields.model_dump(exclude_none=True)}

    if photo:
        data["photo"] = photo

    updated_user = await user_service.update(data=data, item_id=user.id)
    return user_service.to_schema(data=updated_user, schema_type=GetUserSchema)


@router.post("/update-password")
@inject
async def update_password(
        user_service: FromDishka[UserService],
        data: Annotated[UpdatePasswordSchema, Form()],
        user: GetUserSchema = Depends(user_from_token)
) -> SuccessfulMessageSchema:
    await user_service.update_password({'id': user.id, **data.model_dump()})
    return SuccessfulMessageSchema(
        message="Password was updated successfully."
    )

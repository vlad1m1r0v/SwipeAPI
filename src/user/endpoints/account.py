from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from src.core.utils import save_file, generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.services import UserService
from src.user.schemas import (
    GetUserSchema,
    GetUserAccountSchema,
    UpdateUserAccountSchema,
)

router = APIRouter()


@router.patch(
    path="/account",
    response_model=SuccessResponse[GetUserAccountSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True, role=True, user=True),
    tags=["User: Profile"],
)
@inject
async def update_account(
    user_service: FromDishka[UserService],
    email: Optional[str] = Form(default=None),
    name: Optional[str] = Form(default=None),
    phone: Optional[str] = Form(default=None),
    photo: Optional[UploadFile] = File(default=None),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetUserAccountSchema]:
    fields = UpdateUserAccountSchema(
        email=email,
        name=name,
        phone=phone,
        photo=save_file(file=photo) if photo else None,
    )

    result = await user_service.update(
        data={**fields.model_dump(exclude_none=True)}, item_id=user.id
    )

    return SuccessResponse(
        data=user_service.to_schema(data=result, schema_type=GetUserAccountSchema)
    )

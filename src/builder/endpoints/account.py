from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from src.core.utils import save_file, generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import builder_from_token

from src.user.services import UserService
from src.user.schemas import UpdateUserAccountSchema

from src.builder.schemas import GetBuilderSchema

router = APIRouter()


@router.patch(
    path="/account",
    response_model=SuccessResponse[GetBuilderSchema],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    tags=["Builder: Profile"],
)
@inject
async def update_account(
    user_service: FromDishka[UserService],
    email: Optional[str] = Form(default=None),
    name: Optional[str] = Form(default=None),
    phone: Optional[str] = Form(default=None),
    photo: Optional[UploadFile] = File(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetBuilderSchema]:
    fields = UpdateUserAccountSchema(
        email=email,
        name=name,
        phone=phone,
        photo=save_file(file=photo) if photo else None,
    )

    await user_service.update(
        data={**fields.model_dump(exclude_none=True)}, item_id=builder.id
    )

    profile = await user_service.get_builder_profile(item_id=builder.id)
    return SuccessResponse(
        data=user_service.to_schema(data=profile, schema_type=GetBuilderSchema)
    )

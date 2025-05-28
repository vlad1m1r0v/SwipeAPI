from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Query
)

from src.core.schemas import SuccessfulMessageSchema

from src.auth.dependencies import payload_from_token
from src.auth.schemas import (
    TokensSchema,
    BasePayloadSchema,
    UpdatePasswordSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)
from src.auth.services import AuthService
from src.auth.enums import TokenType

from src.auth.endpoints.users import router as user_router
from src.auth.endpoints.admins import router as admin_router

from src.users.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(user_router)
router.include_router(admin_router)


@router.post('/tokens/refresh', response_model=TokensSchema)
@inject
def refresh_tokens(
        auth_service: FromDishka[AuthService],
        payload: BasePayloadSchema = Depends(payload_from_token(TokenType.REFRESH_TOKEN)),
):
    return auth_service.generate_tokens(payload)


@router.post("/password/update")
@inject
async def update_password(
        user_service: FromDishka[UserService],
        data: Annotated[UpdatePasswordSchema, Form()],
        payload: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN))
) -> SuccessfulMessageSchema:
    await user_service.update_password(item_id=payload.id, data=data.model_dump())
    return SuccessfulMessageSchema(
        message="Password was updated successfully."
    )


@router.post("/password/forgot")
@inject
async def forgot_password(
        auth_service: FromDishka[AuthService],
        data: Annotated[ForgotPasswordSchema, Form()],
):
    await auth_service.send_forgot_password_email(data)
    return SuccessfulMessageSchema(
        message="Password reset email was sent successfully."
    )


@router.post("/password/reset")
@inject
async def reset_password(
        auth_service: FromDishka[AuthService],
        token: str = Query(),
        new_password: str = Form(),
        confirm_password: str = Form(...),
):
    data = ResetPasswordSchema(
        token=token,
        new_password=new_password,
        confirm_password=confirm_password,
    )

    await auth_service.reset_password(data=data)

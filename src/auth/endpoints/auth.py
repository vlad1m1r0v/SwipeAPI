from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Body, Query
from starlette import status

from src.core.schemas import SuccessResponse, success_response
from src.core.utils import generate_examples

from src.auth.dependencies import payload_from_token
from src.auth.schemas import (
    TokensSchema,
    BasePayloadSchema,
    UpdatePasswordSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)
from src.auth.services import AuthService
from src.auth.enums import TokenType
from src.auth.exceptions import SignatureExpiredException, BadSignatureException

from src.auth.endpoints.user import router as user_router
from src.auth.endpoints.admin import router as admin_router
from src.auth.endpoints.builder import router as builder_router

from src.user.services import UserService
from src.user.exceptions import UserDoesNotExistException

router = APIRouter(prefix="/auth")

router.include_router(user_router)
router.include_router(admin_router)
router.include_router(builder_router)


@router.post(
    path="/tokens/refresh",
    response_model=SuccessResponse[TokensSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True),
    tags=["Auth: Common"],
)
@inject
def refresh_tokens(
    auth_service: FromDishka[AuthService],
    payload: BasePayloadSchema = Depends(payload_from_token(TokenType.REFRESH_TOKEN)),
) -> SuccessResponse[TokensSchema]:
    return success_response(value=auth_service.generate_tokens(payload))


@router.post(
    path="/password/update",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True),
    tags=["Auth: Common"],
)
@inject
async def update_password(
    user_service: FromDishka[UserService],
    data: UpdatePasswordSchema,
    payload: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse:
    await user_service.update_password(item_id=payload.id, data=data.model_dump())
    return success_response(message="Password updated successfully.")


@router.post(
    path="/password/forgot",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(UserDoesNotExistException),
    tags=["Auth: Common"],
)
@inject
async def forgot_password(
    auth_service: FromDishka[AuthService],
    data: ForgotPasswordSchema,
) -> SuccessResponse:
    await auth_service.send_forgot_password_email(data)
    return success_response(message="Password reset email was sent successfully.")


@router.post(
    path="/password/reset",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(SignatureExpiredException, BadSignatureException),
    tags=["Auth: Common"],
)
@inject
@inject
async def reset_password(
    auth_service: FromDishka[AuthService],
    new_password: str = Body(),
    confirm_password: str = Body(),
    token: str = Query(),
) -> SuccessResponse:
    data = ResetPasswordSchema(
        token=token,
        new_password=new_password,
        confirm_password=confirm_password,
    )

    await auth_service.reset_password(data=data)
    return success_response(message="Password updated successfully.")

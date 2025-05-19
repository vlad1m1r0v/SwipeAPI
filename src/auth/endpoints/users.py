from typing import Annotated

from fastapi import (
    APIRouter,
    Form,
    Depends
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.dependencies import user_from_token
from src.auth.services import AuthService
from src.auth.schemas import (
    TokensSchema,
    RegisterSchema,
    LoginSchema
)
from src.auth.enums import TOKEN_TYPE

from src.users.schemas import GetUserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=TokensSchema)
@inject
async def register_user(
        data: Annotated[RegisterSchema, Form()],
        auth_service: FromDishka[AuthService],
):
    return await auth_service.register_user(data=data)


@router.post("/login", response_model=TokensSchema)
@inject
async def login_user(
        data: Annotated[LoginSchema, Form()],
        auth_service: FromDishka[AuthService],
):
    return await auth_service.login_user(data=data)


@router.post('/tokens/refresh', response_model=TokensSchema)
@inject
def refresh_tokens(
        auth_service: FromDishka[AuthService],
        user: GetUserSchema = Depends(user_from_token(TOKEN_TYPE.REFRESH_TOKEN)),
):
    return auth_service.generate_tokens(user)

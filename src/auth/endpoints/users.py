from typing import Annotated

from fastapi import (
    APIRouter,
    Form
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.services import AuthService
from src.auth.schemas import (
    TokensSchema,
    RegisterSchema,
    LoginSchema
)

router = APIRouter(prefix="/users")


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
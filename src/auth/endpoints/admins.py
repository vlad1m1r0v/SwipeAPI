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

router = APIRouter(prefix="/admins")


@router.post("/register", response_model=TokensSchema)
@inject
async def register_admin(
        data: Annotated[RegisterSchema, Form()],
        auth_service: FromDishka[AuthService],
):
    return await auth_service.register_admin(data=data)


@router.post("/login", response_model=TokensSchema)
@inject
async def login_admin(
        data: Annotated[LoginSchema, Form()],
        auth_service: FromDishka[AuthService],
):
    return await auth_service.login_admin(data=data)

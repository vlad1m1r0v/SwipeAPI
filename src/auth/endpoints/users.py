from fastapi import APIRouter

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema, RegisterSchema, LoginSchema

router = APIRouter(prefix="/users", tags=["Auth: Users"])


@router.post("/register", response_model=TokensSchema)
@inject
async def register_user(
    data: RegisterSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.register_user(data=data)


@router.post("/login", response_model=TokensSchema)
@inject
async def login_user(
    data: LoginSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.login_user(data=data)

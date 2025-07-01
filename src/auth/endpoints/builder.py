from fastapi import APIRouter

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema, RegisterSchema, LoginSchema

router = APIRouter(prefix="/builder", tags=["Auth: Builder"])


@router.post("/register", response_model=TokensSchema)
@inject
async def register_builder(
    data: RegisterSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.register_builder(data=data)


@router.post("/login", response_model=TokensSchema)
@inject
async def login_builder(
    data: LoginSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.login_builder(data=data)

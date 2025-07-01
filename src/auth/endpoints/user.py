from fastapi import APIRouter

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.core.utils import generate_examples

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema, RegisterSchema, LoginSchema

from src.user.exceptions import (
    UserDoesNotExistException,
    UserBlacklistedException,
    SubscriptionExpiredException,
)

router = APIRouter(prefix="/user", tags=["Auth: User"])


@router.post("/register", responses=generate_examples())
@inject
async def register_user(
    data: RegisterSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.register_user(data=data)


@router.post(
    "/login",
    response_model=TokensSchema,
    responses=generate_examples(
        UserDoesNotExistException,
        SubscriptionExpiredException,
        UserBlacklistedException,
    ),
)
@inject
async def login_user(
    data: LoginSchema,
    auth_service: FromDishka[AuthService],
):
    return await auth_service.login_user(data=data)

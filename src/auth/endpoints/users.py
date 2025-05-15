from typing import Annotated

from fastapi import APIRouter, Form

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema

from src.users.schemas import (
    CreateUserSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=TokensSchema)
@inject
async def register_user(
        data: Annotated[CreateUserSchema, Form()],
        auth_service: FromDishka[AuthService],
):
    return await auth_service.register_user(data=data)

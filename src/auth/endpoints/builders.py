from typing import Annotated

from fastapi import APIRouter, Form

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema, RegisterSchema, LoginSchema

router = APIRouter(prefix="/builders")


@router.post("/register", response_model=TokensSchema)
@inject
async def register_builder(
    data: Annotated[RegisterSchema, Form()],
    auth_service: FromDishka[AuthService],
):
    return await auth_service.register_builder(data=data)


@router.post("/login", response_model=TokensSchema)
@inject
async def login_builder(
    data: Annotated[LoginSchema, Form()],
    auth_service: FromDishka[AuthService],
):
    return await auth_service.login_builder(data=data)

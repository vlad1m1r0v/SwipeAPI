from fastapi import APIRouter, status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse, success_response

from src.auth.services import AuthService
from src.auth.schemas import TokensSchema, RegisterSchema, LoginSchema

from src.user.exceptions import (
    UserDoesNotExistException,
    IncorrectPasswordException,
    UserAlreadyExistsException,
)

router = APIRouter(prefix="/user", tags=["Auth: User"])


@router.post(
    path="/register",
    response_model=SuccessResponse[TokensSchema],
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(UserAlreadyExistsException),
)
@inject
async def register_user(
    data: RegisterSchema,
    auth_service: FromDishka[AuthService],
):
    return success_response(
        value=await auth_service.register_user(data=data),
        message="User registered successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    path="/login",
    response_model=SuccessResponse[TokensSchema],
    responses=generate_examples(
        UserDoesNotExistException, IncorrectPasswordException, user=True, role=True
    ),
)
@inject
async def login_user(
    data: LoginSchema,
    auth_service: FromDishka[AuthService],
):
    return success_response(
        value=await auth_service.login_user(data=data),
        message="User logged in successfully.",
    )

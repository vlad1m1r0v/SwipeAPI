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

router = APIRouter(prefix="/builder", tags=["Auth: Builder"])


@router.post(
    path="/register",
    response_model=SuccessResponse[TokensSchema],
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(UserAlreadyExistsException),
)
@inject
async def register_builder(
    data: RegisterSchema,
    auth_service: FromDishka[AuthService],
) -> SuccessResponse[TokensSchema]:
    return success_response(
        value=await auth_service.register_builder(data=data),
        message="Builder registered successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    path="/login",
    response_model=SuccessResponse[TokensSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        UserDoesNotExistException, IncorrectPasswordException, role=True
    ),
)
@inject
async def login_builder(
    data: LoginSchema,
    auth_service: FromDishka[AuthService],
) -> SuccessResponse[TokensSchema]:
    return success_response(
        value=await auth_service.login_builder(data=data),
        message="Builder logged in successfully.",
    )

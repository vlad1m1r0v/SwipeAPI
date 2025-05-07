from fastapi import APIRouter, Response, status
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.users.schemas import UserCreateSchema
from src.users.services import UserService

from src.auth.services import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_user(
        data: UserCreateSchema,
        user_service: FromDishka[UserService],
        auth_service: FromDishka[AuthService],
) -> Response:
    hashed_password = auth_service.hash_password(data.password)
    updated_data = data.model_copy(update={"password": hashed_password.decode()})

    await user_service.create(updated_data)
    return Response(status_code=status.HTTP_201_CREATED)

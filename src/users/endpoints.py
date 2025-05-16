from typing import Optional

from fastapi import (
    APIRouter,
    Depends, UploadFile
)

from src.auth.dependencies import user_from_token

from src.users.dependencies import update_user_form
from src.users.schemas import (
    UpdateUserSchema,
    GetUserSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/account")
async def update_account(
        user: GetUserSchema = Depends(user_from_token),
        data: tuple[UpdateUserSchema, Optional[UploadFile]] = Depends(update_user_form),
) -> GetUserSchema:
    return user

from fastapi import APIRouter, Depends

from src.auth.dependencies import user_from_token

from src.users.schemas import GetUserSchema

router = APIRouter()


@router.get("/profile")
def get_profile(user: GetUserSchema = Depends(user_from_token)) -> GetUserSchema:
    return user

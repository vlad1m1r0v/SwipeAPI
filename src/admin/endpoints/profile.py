from fastapi import APIRouter, Depends

from src.auth.dependencies import admin_from_token

from src.admin.schemas import GetAdminSchema

router = APIRouter()


@router.get("/profile", tags=["Admin: Profile"])
def get_profile(admin: GetAdminSchema = Depends(admin_from_token)) -> GetAdminSchema:
    return admin

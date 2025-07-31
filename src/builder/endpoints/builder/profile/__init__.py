from fastapi import APIRouter, Depends

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import builder_from_token

from src.builder.schemas import GetBuilderSchema

from .account import router as account_router
from .contact import router as contact_router
from .advantages import router as advantages_router
from .infrastructure import router as infrastructure_router
from .formalization_and_payment_settings import (
    router as formalization_and_payment_settings_router,
)
from .news import router as news_router
from .document import router as document_router
from .gallery import router as gallery_router


router = APIRouter(prefix="/profile", tags=["Builder: Profile"])


@router.get(
    path="",
    response_model=SuccessResponse[GetBuilderSchema],
    responses=generate_examples(auth=True, role=True),
)
def get_profile(
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetBuilderSchema]:
    return SuccessResponse(data=builder)


router.include_router(account_router)
router.include_router(contact_router)
router.include_router(advantages_router)
router.include_router(infrastructure_router)
router.include_router(formalization_and_payment_settings_router)
router.include_router(news_router)
router.include_router(document_router)
router.include_router(gallery_router)

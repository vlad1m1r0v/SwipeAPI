from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.schemas import Base64Item, GetGalleryImageSchema, SuccessResponse
from src.core.utils import generate_examples
from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)

from src.auth.dependencies import builder_from_token

from src.builder.services import GalleryService
from src.builder.schemas import GetBuilderSchema

router = APIRouter()


@router.patch(
    path="/gallery",
    tags=["Builder: Gallery"],
    response_model=SuccessResponse[List[GetGalleryImageSchema]],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_gallery(
    gallery_service: FromDishka[GalleryService],
    media_set: List[Base64Item],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[List[GetGalleryImageSchema]]:
    gallery = await gallery_service.update_gallery(
        complex_id=builder.complex.id, media_set=media_set
    )
    return SuccessResponse(data=gallery)

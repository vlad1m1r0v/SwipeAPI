from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.exceptions import (
    NotFoundException,
    IntegrityErrorException,
    IsNotOwnerException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import admin_from_token

from src.admin.schemas import GetAdminSchema

from src.announcements.services import AnnouncementComplaintService
from src.announcements.dependencies import check_admin_owns_complaint
from src.announcements.schemas import GetComplaintSchema, CreateComplaintSchema

router = APIRouter(prefix="/complaints", tags=["Admin: Complaints"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetComplaintSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_complaints(
    complaint_service: FromDishka[AnnouncementComplaintService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    admin: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse[OffsetPagination[GetComplaintSchema]]:
    results, total = await complaint_service.get_admin_complaints(
        limit=limit, offset=offset, admin_id=admin.id
    )
    return SuccessResponse(
        data=complaint_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetComplaintSchema,
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    response_model=SuccessResponse[GetComplaintSchema],
)
@inject
async def create_complaint(
    complaint_service: FromDishka[AnnouncementComplaintService],
    data: CreateComplaintSchema = Body(),
    admin: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse[GetComplaintSchema]:
    created = await complaint_service.create(
        data={"user_id": admin.id, **data.model_dump()}
    )
    complaint = await complaint_service.get_complaint(created.id)
    return SuccessResponse(
        data=complaint_service.to_schema(data=complaint, schema_type=GetComplaintSchema)
    )


@router.delete(
    path="/{complaint_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_complaint(
    complaint_service: FromDishka[AnnouncementComplaintService],
    complaint_id: int,
    _: GetAdminSchema = Depends(check_admin_owns_complaint),
):
    await complaint_service.delete(item_id=complaint_id)
    return SuccessResponse(message="Complaint has been deleted successfully.")

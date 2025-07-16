from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.schemas import AddToComplexRequestSchema, GetBuilderSchema

from src.apartments.services import AddToComplexRequestService

from src.auth.dependencies import builder_from_token

router = APIRouter(
    prefix="/add-to-complex-requests", tags=["Builder: Add to complex requests"]
)


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[AddToComplexRequestSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_add_to_complex_requests(
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[AddToComplexRequestSchema]]:
    results, total = await add_to_complex_request_service.get_requests(
        limit=limit, offset=offset, complex_id=builder.complex.id
    )
    return SuccessResponse(
        data=add_to_complex_request_service.to_schema(
            data=results, total=total, schema_type=AddToComplexRequestSchema
        )
    )


@router.post(
    path="/{request_id}/approve",
    response_model=SuccessResponse,
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def approve_add_to_complex_requests(
    request_id: int,
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[AddToComplexRequestSchema]]:
    await add_to_complex_request_service.approve(request_id)
    return SuccessResponse(
        message="User request has been approved successfully.",
    )


@router.post(
    path="/{request_id}/reject",
    response_model=SuccessResponse,
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def reject_add_to_complex_requests(
    request_id: int,
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[AddToComplexRequestSchema]]:
    await add_to_complex_request_service.delete(item_id=request_id)
    return SuccessResponse(
        message="User request has been rejected successfully.",
    )

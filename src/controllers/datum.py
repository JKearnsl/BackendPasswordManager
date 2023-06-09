import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views import DatumListResponse

router = APIRouter()


@router.get("/list", response_model=DatumListResponse, status_code=http_status.HTTP_200_OK)
async def get_list(
        resource_id: uuid.UUID,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        order_by: str = "id",
        services: ServiceFactory = Depends(get_services)
):
    return DatumListResponse(message=await services.datum.get_list(
        resource_id=resource_id,
        page=page,
        per_page=per_page,
        query=query,
        order_by=order_by
    ))


@router.post("/new", status_code=http_status.HTTP_201_CREATED, response_model=uuid.UUID)
async def create(resource_id: uuid.UUID, data: schemas.NewDatum, services: ServiceFactory = Depends(get_services)):
    return await services.datum.create_datum(resource_id, data)

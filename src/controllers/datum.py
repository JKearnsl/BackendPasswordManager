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
        services: ServiceFactory = Depends(get_services)
):
    return DatumListResponse(message=await services.datum.get_list(
        resource_id=str(resource_id),
        page=page,
        per_page=per_page
    ))


@router.post("/new", status_code=http_status.HTTP_201_CREATED)
async def create(resource_id: uuid.UUID, data: schemas.NewDatum, services: ServiceFactory = Depends(get_services)):
    await services.datum.create_datum(str(resource_id), data)

import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views import PasswordListResponse

router = APIRouter()


@router.get("/list", response_model=PasswordListResponse, status_code=http_status.HTTP_200_OK)
async def get_user(
        resource_id: uuid.UUID,
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        order_by: str = "id",
        services: ServiceFactory = Depends(get_services)
):
    return PasswordListResponse(message=await services.password.get_list(
        resource_id=resource_id,
        page=page,
        per_page=per_page,
        query=query,
        order_by=order_by
    ))

@router.get("/new", status_code=http_status.HTTP_201_CREATED)
async def create(resource_id: uuid.UUID, data: schemas.NewPassword, services: ServiceFactory = Depends(get_services)):
    await services.password.create_password(resource_id, data)
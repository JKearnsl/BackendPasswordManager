import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views import ResourceListResponse, ResourceResponse

router = APIRouter()


@router.get("/list", response_model=ResourceListResponse, status_code=http_status.HTTP_200_OK)
async def get_list(
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        order_by: str = "created_at",
        services: ServiceFactory = Depends(get_services)
):
    return ResourceListResponse(message=await services.resource.get_list(
        page=page,
        per_page=per_page,
        query=query,
        order_by=order_by
    ))


@router.post("/new", status_code=http_status.HTTP_201_CREATED, response_model=ResourceResponse)
async def create(data: schemas.NewResource, services: ServiceFactory = Depends(get_services)):
    return ResourceResponse(message=await services.resource.create_resource(data))


@router.delete("/delete", status_code=http_status.HTTP_204_NO_CONTENT)
async def delete(resource_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    await services.resource.delete_resource(str(resource_id))


@router.put("/update", status_code=http_status.HTTP_204_NO_CONTENT)
async def update(
        resource_id: uuid.UUID,
        data: schemas.UpdateResource,
        services: ServiceFactory = Depends(get_services)
):
    await services.resource.update_resource(str(resource_id), data)

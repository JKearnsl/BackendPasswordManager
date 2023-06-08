import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi.requests import Request
from fastapi.responses import Response

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserResponse
router = APIRouter()


@router.get("/current", response_model=UserResponse, status_code=http_status.HTTP_200_OK)
async def get_current_user(services: ServiceFactory = Depends(get_services)):
    return UserResponse(message=await services.user.get_me())


@router.post("/update", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(data: schemas.UserUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_me(data)


@router.delete("/delete", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, response: Response, services: ServiceFactory = Depends(get_services)):
    await services.user.delete_me()
    await services.auth.logout(request, response)  # TODO: разлогин через Redis

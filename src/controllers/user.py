from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi.requests import Request
from fastapi.responses import Response

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserResponse, KeysResponse

router = APIRouter()


@router.get("/current", response_model=UserResponse, status_code=http_status.HTTP_200_OK)
async def get_current_user(services: ServiceFactory = Depends(get_services)):
    return UserResponse(message=await services.user.get_me())


@router.put("/update/username", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_username(data: schemas.UsernameUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_username(data)


@router.put("/update/keys", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_keys(data: schemas.UserKeysUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_keys(data)


@router.put("/update/password", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_password(
        new_hashed_password: str,
        old_hashed_password: str,
        new_enc_private_key: str,
        services: ServiceFactory = Depends(get_services)
):
    await services.user.update_password(new_hashed_password, old_hashed_password, new_enc_private_key)


@router.get("/keys", response_model=KeysResponse, status_code=http_status.HTTP_200_OK)
async def get_keys(services: ServiceFactory = Depends(get_services)):
    return KeysResponse(message=await services.user.get_keys())


@router.delete("/delete", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, response: Response, services: ServiceFactory = Depends(get_services)):
    await services.user.delete_me()
    await services.auth.logout(request, response)

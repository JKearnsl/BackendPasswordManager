from fastapi import APIRouter

from src.controllers import auth
from src.controllers import user
from src.controllers import datum
from src.controllers import resource
from src.controllers import stats


def reg_root_api_router(is_debug: bool) -> APIRouter:
    root_api_router = APIRouter(prefix="/api/v1" if is_debug else "")

    root_api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
    root_api_router.include_router(user.router, prefix="/user", tags=["User"])
    root_api_router.include_router(resource.router, prefix="/resource", tags=["Resource"])
    root_api_router.include_router(datum.router, prefix="/password", tags=["Datum"])
    root_api_router.include_router(stats.router, prefix="", tags=["Stats"])

    return root_api_router

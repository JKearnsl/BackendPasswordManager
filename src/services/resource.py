import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.repository import ResourceRepo


class ResourceApplicationService:

    def __init__(self, resource_repo: ResourceRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = resource_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.USER])
    async def get_list(self, page: int, per_page: int, query: str | None, order_by: str) -> list[schemas.Resource]:
        return [schemas.Resource.from_orm(resource) for resource in await self._repo.list()]

    @filters(roles=[UserRole.USER])
    def create_resource(self, data: schemas.NewResource):
        pass

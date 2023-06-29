from src.exceptions import AccessDenied, NotFound, BadRequest, AlreadyExists
from src.models import schemas
from src.models.auth import BaseUser
from src.models.enums.role import UserRole
from src.services.auth.filters import role_filter
from src.services.repository import ResourceRepo


class ResourceApplicationService:

    def __init__(self, resource_repo: ResourceRepo, *, current_user: BaseUser, debug: bool = False):
        self._repo = resource_repo
        self._current_user = current_user
        self._debug = debug

    @role_filter(UserRole.USER)
    async def get_list(
            self,
            page: int,
            per_page: int,
            query: str | None = None,
            order_by: str = "created_at"
    ) -> list[schemas.Resource]:
        if page < 1:
            raise NotFound("Страница не найдена")
        if per_page < 1:
            raise BadRequest("Неверное количество элементов на странице")

        allowed_order_by = ["created_at", "updated_at"]
        if order_by not in allowed_order_by:
            raise BadRequest(f"Инвалидный параметр order_by, доступные значения: {allowed_order_by}")

        limit = per_page
        offset = (page - 1) * per_page
        if not query:
            rows = await self._repo.get_all(
                owner_id=self._current_user.id, limit=limit, offset=offset, order_by=order_by
            )
        else:
            rows = await self._repo.search(
                owner_id=self._current_user.id, query=query, limit=limit, offset=offset, order_by=order_by
            )
        return [schemas.Resource.from_orm(resource) for resource in rows]

    @role_filter(UserRole.USER)
    async def create_resource(self, data: schemas.NewResource):
        title = data.title
        result = await self._repo.get(owner_id=self._current_user.id, title=title)
        if result:
            raise AlreadyExists(f"Ресурс {title!r} уже существует")

        data = await self._repo.create(owner_id=self._current_user.id, title=data.title)
        return schemas.Resource.from_orm(data)

    @role_filter(UserRole.USER)
    async def delete_resource(self, resource_id: str):
        resource = await self._repo.get(id=resource_id)
        if not resource:
            raise NotFound(f"Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Нет доступа к ресурсу")

        await self._repo.delete(id=resource_id)

    @role_filter(UserRole.USER)
    async def update_resource(self, resource_id: str, data: schemas.UpdateResource):
        resource = await self._repo.get(id=resource_id)
        if not resource:
            raise NotFound(f"Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Нет доступа к ресурсу")

        await self._repo.update(id=resource_id, title=data.title)

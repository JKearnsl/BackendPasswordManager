from src.exceptions import AccessDenied, NotFound, BadRequest
from src.models import schemas
from src.models.auth import BaseUser
from src.models.enums.role import UserRole
from src.services.auth.filters import role_filter
from src.services.repository import DatumRepo, ResourceRepo


class DatumApplicationService:

    def __init__(
            self,
            datum_repo: DatumRepo,
            *,
            resource_repo: ResourceRepo,
            current_user: BaseUser,
            debug: bool = True
    ):
        self._repo = datum_repo
        self._resource_repo = resource_repo
        self._current_user = current_user
        self._debug = debug

    @role_filter(UserRole.USER)
    async def get_list(self, resource_id: str, page: int, per_page: int) -> list[schemas.Datum]:
        if page < 1:
            raise NotFound("Страница не найдена")
        if per_page < 1:
            raise BadRequest("Неверное количество элементов на странице")

        resource = await self._resource_repo.get(id=resource_id)
        if not resource:
            raise NotFound("Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Вы не являетесь владельцем ресурса")

        return await self._repo.get_all(
            limit=per_page,
            offset=(page - 1) * per_page,
            order_by="created_at",
            resource_id=resource_id
        )

    @role_filter(UserRole.USER)
    async def create_datum(self, resource_id: str, data: schemas.NewDatum):
        if not data.username and not data.enc_password:
            raise BadRequest("Отсутствуют данные")

        resource = await self._resource_repo.get(id=resource_id)
        if not resource:
            raise NotFound("Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Вы не являетесь владельцем ресурса")

        result = await self._repo.create(resource_id=resource_id, username=data.username, enc_password=data.enc_password)
        return schemas.Datum.from_orm(result)

    @role_filter(UserRole.USER)
    async def delete_datum(self, datum_id: str):
        datum = await self._repo.get(id=datum_id)
        if not datum:
            raise NotFound("Запись не найдена")

        resource = await self._resource_repo.get(id=datum.resource_id)
        if not resource:
            raise NotFound("Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Вы не являетесь владельцем ресурса")

        await self._repo.delete(id=datum_id)

    @role_filter(UserRole.USER)
    async def update_datum(self, datum_id: str, data: schemas.UpdateDatum):
        datum = await self._repo.get(id=datum_id)
        if not datum:
            raise NotFound("Запись не найдена")

        resource = await self._resource_repo.get(id=datum.resource_id)
        if not resource:
            raise NotFound("Ресурс не найден")

        if resource.owner_id != self._current_user.id:
            raise AccessDenied("Вы не являетесь владельцем ресурса")

        await self._repo.update(id=datum_id, username=data.username, enc_password=data.enc_password)

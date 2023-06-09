import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.repository import DatumRepo


class DatumApplicationService:

    def __init__(self, datum_repo: DatumRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = datum_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.USER])
    async def get_list(self, page: int, per_page: int, query: str | None, order_by: str) -> list[schemas.Datum]:
        return [schemas.Datum.from_orm(datum) for datum in await self._repo.list()]

    @filters(roles=[UserRole.USER])
    def create_datum(self,resource_id: uuid.UUID, data: schemas.NewDatum):
        pass
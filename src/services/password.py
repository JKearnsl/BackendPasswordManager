import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.repository import PasswordRepo


class PasswordApplicationService:

    def __init__(self, password_repo: PasswordRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = password_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.USER])
    async def get_list(self, page: int, per_page: int, query: str | None, order_by: str) -> list[schemas.Password]:
        return [schemas.Password.from_orm(password) for password in await self._repo.list()]

    @filters(roles=[UserRole.USER])
    def create_password(self,resource_id: uuid.UUID, data: schemas.NewPassword):
        pass
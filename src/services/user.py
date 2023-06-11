import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.filters import role_filter
from src.services.repository import UserRepo

class UserApplicationService:

    def __init__(self, user_repo: UserRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = user_repo
        self._current_user = current_user
        self._debug = debug

    @role_filter(UserRole.USER)
    async def get_me(self) -> schemas.User:
        return schemas.User.from_orm(await self._repo.get(id=self._current_user.id))

    @role_filter(UserRole.USER)
    async def get_keys(self) -> schemas.Keys:
        return schemas.Keys.from_orm(await self._repo.get(id=self._current_user.id))

    @role_filter(UserRole.USER)
    async def update_me(self, data: schemas.UserUpdate) -> None:
        await self._repo.update(
            id=self._current_user.id,
            **data.dict(exclude_unset=True)
        )

    @role_filter(UserRole.USER)
    async def delete_me(self) -> None:
        await self._repo.delete(id=self._current_user.id)

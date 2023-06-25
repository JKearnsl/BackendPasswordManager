from typing import Optional

from src.exceptions import AccessDenied, ConflictError
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.filters import role_filter
from src.services.repository import UserRepo


# todo: тип current_user определен неправильно

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
    async def update_username(self, data: schemas.UsernameUpdate) -> None:
        some_user = await self._repo.get_by_username_insensitive(username=data.username)
        if some_user:
            raise ConflictError(f"Имя {data.username!r} уже занято")

        user = await self._repo.get(id=self._current_user.id)
        if data.old_hashed_password != user.hashed_password:
            raise AccessDenied("Неверный пароль")

        await self._repo.update(
            id=self._current_user.id,
            username=data.username,
            hashed_password=data.new_hashed_password
        )

    @role_filter(UserRole.USER)
    async def update_password(self, new_hashed_password: str, old_hashed_password: str, new_enc_private_key: str):
        user = await self._repo.get(id=self._current_user.id)
        if user.hashed_password != old_hashed_password:
            raise AccessDenied("Неверный пароль")

        await self._repo.update(
            id=self._current_user.id,
            hashed_password=new_hashed_password,
            enc_private_key=new_enc_private_key
        )

    @role_filter(UserRole.USER)
    async def update_keys(self, data: schemas.UserKeysUpdate) -> None:
        user = await self._repo.get(id=self._current_user.id)
        if data.hashed_password != user.hashed_password:
            raise AccessDenied("Неверный пароль")

        await self._repo.update(
            id=self._current_user.id,
            public_key=data.public_key,
            enc_private_key=data.enc_private_key
        )

    @role_filter(UserRole.USER)
    async def delete_me(self) -> None:
        await self._repo.delete(id=self._current_user.id)

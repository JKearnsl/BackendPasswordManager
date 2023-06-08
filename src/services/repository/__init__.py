from .user import UserRepo
from .password import PasswordRepo


class RepoFactory:
    def __init__(self, session, debug: bool = False):
        self._session = session
        self._debug = debug

    @property
    def user(self) -> UserRepo:
        return UserRepo(self._session)

    @property
    def password(self) -> PasswordRepo:
        return PasswordRepo(self._session)

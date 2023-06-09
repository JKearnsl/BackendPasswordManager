from .user import UserRepo
from .password import DatumRepo
from .resource import ResourceRepo


class RepoFactory:
    def __init__(self, session, debug: bool = False):
        self._session = session
        self._debug = debug

    @property
    def user(self) -> UserRepo:
        return UserRepo(self._session)

    @property
    def datum(self) -> DatumRepo:
        return DatumRepo(self._session)

    @property
    def resource(self) -> ResourceRepo:
        return ResourceRepo(self._session)

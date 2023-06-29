from src.models.auth import BaseUser
from . import repository
from . import auth
from .datum import DatumApplicationService
from .resource import ResourceApplicationService
from .user import UserApplicationService


class ServiceFactory:
    def __init__(
            self,
            repo_factory: repository.RepoFactory,
            *,
            current_user: BaseUser,
            config, redis_client,
            debug: bool = False
    ):
        self._repo = repo_factory
        self._current_user = current_user
        self._config = config
        self._redis_client = redis_client
        self._debug = debug

    @property
    def user(self) -> UserApplicationService:
        return UserApplicationService(self._repo.user, current_user=self._current_user, debug=self._debug)

    @property
    def auth(self) -> auth.AuthApplicationService:
        return auth.AuthApplicationService(
            jwt=auth.JWTManager(config=self._config, debug=self._debug),
            session=auth.SessionManager(redis_client=self._redis_client, config=self._config, debug=self._debug),
            user_repo=self._repo.user,
            current_user=self._current_user,
            debug=self._debug
        )

    @property
    def datum(self) -> DatumApplicationService:
        return DatumApplicationService(
            self._repo.datum,resource_repo=self._repo.resource, current_user=self._current_user, debug=self._debug
        )

    @property
    def resource(self) -> ResourceApplicationService:
        return ResourceApplicationService(self._repo.resource, current_user=self._current_user, debug=self._debug)

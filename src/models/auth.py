from abc import ABC, abstractmethod

from starlette import authentication

from src.models.enums import UserRole


class BaseUser(ABC, authentication.BaseUser):

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def username(self) -> str:
        pass

    @property
    @abstractmethod
    def role(self):
        pass

    @property
    @abstractmethod
    def access_exp(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}>({self.display_name})"


class AuthenticatedUser(BaseUser):
    def __init__(self, id: str, username: str, role_value: int, exp: int, **kwargs):
        self._id = id
        self._username = username
        self._role_value = role_value
        self._exp = exp

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> str:
        return self._id

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self.username

    @property
    def role(self) -> UserRole:
        return UserRole(self._role_value)

    @property
    def access_exp(self) -> int:
        return self._exp

    def __eq__(self, other):
        return isinstance(other, AuthenticatedUser) and self._id == other.id

    def __hash__(self):
        return hash(self._id)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self._id}, username={self._username})>"


class UnauthenticatedUser(BaseUser):
    def __init__(self, exp: int = None):
        self._exp = exp

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return "Guest"

    @property
    def identity(self) -> None:
        return None

    @property
    def id(self) -> None:
        return None

    @property
    def username(self) -> None:
        return None

    @property
    def role(self) -> UserRole:
        return UserRole.GUEST

    @property
    def access_exp(self) -> int | None:
        return self._exp

    def __eq__(self, other):
        return isinstance(other, UnauthenticatedUser)

    def __repr__(self):
        return f"<{self.__class__.__name__}>({self.display_name})"

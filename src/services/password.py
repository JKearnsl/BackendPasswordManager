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

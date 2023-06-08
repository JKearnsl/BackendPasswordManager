from src.views.base import BaseView
from src.models.schemas import Password


class PasswordListResponse(BaseView):
    message: list[Password | None]

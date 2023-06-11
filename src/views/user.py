from src.views.base import BaseView
from src.models.schemas import User, Keys


class UserResponse(BaseView):
    message: User


class KeysResponse(BaseView):
    message: Keys

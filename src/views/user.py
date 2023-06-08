from src.views.base import BaseView
from src.models.schemas import User


class UserResponse(BaseView):
    message: User

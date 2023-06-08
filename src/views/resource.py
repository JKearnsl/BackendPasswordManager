from src.views.base import BaseView
from src.models.schemas import Resource


class ResourceListResponse(BaseView):
    message: list[Resource | None]

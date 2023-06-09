from src.views.base import BaseView
from src.models.schemas import Datum


class DatumListResponse(BaseView):
    message: list[Datum | None]

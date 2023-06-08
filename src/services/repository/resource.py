from typing import Optional

from sqlalchemy import insert, update, delete, func, select

from src.models import tables
from src.services.repository.base import BaseRepository


class ResourceRepo(BaseRepository[tables.Resource]):
    table = tables.Resource

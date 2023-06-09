from sqlalchemy import insert, update, delete, func, select, text

from src.models import tables
from src.services.repository.base import BaseRepository


class ResourceRepo(BaseRepository[tables.Resource]):
    table = tables.Resource

    async def search(self, query: str, limit: int = 100, offset: int = 0, order_by: str = "created_at", **kwargs):
        query = f"%{query}%"
        result = await self._session.execute(
            select(self.table).where(
                self.table.title.ilike(query)
            ).filter_by(**kwargs).order_by(text(order_by)).limit(limit).offset(offset)
        )
        return result.scalars().all()
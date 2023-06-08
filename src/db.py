import urllib.parse
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base


def create_sqlite_async_session(
        database: str,
        echo: bool = False
) -> Tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///{database}".format(
            database=database
        ),
        echo=echo,
        future=True
    )
    return engine, async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()

import urllib.parse
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base


def create_sqlite_async_session(database: str, echo: bool = False) -> Tuple[AsyncEngine, sessionmaker]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///{database}".format(
            database=database
        ),
        echo=echo,
        future=True
    )
    return engine, sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()

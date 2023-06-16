import os
from functools import lru_cache
from typing import Optional
from dataclasses import dataclass
import configparser

from src.version import __version__


@dataclass
class RedisConfig:
    HOST: Optional[str]
    PASSWORD: Optional[str]
    USERNAME: Optional[str]
    PORT: Optional[int] = 6379


@dataclass
class DbConfig:
    REDIS: Optional[RedisConfig]


@dataclass
class Contact:
    NAME: Optional[str]
    URL: Optional[str]
    EMAIL: Optional[str]


@dataclass
class JWT:
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str


@dataclass
class Base:
    TITLE: Optional[str]
    DESCRIPTION: Optional[str]
    VERSION: Optional[str]
    JWT: JWT
    CONTACT: Contact


@dataclass
class Config:
    DEBUG: bool
    IS_SECURE_COOKIE: bool
    BASE: Base
    DB: DbConfig


def str_to_bool(value: str) -> bool:
    return value.lower() in ("yes", "true", "t", "1")


@lru_cache()
def load_ini_config(path: str | os.PathLike, encoding="utf-8") -> Config:
    """
    Loads config from file

    :param path: *.ini
    :param encoding:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(filenames=path, encoding=encoding)

    return Config(
        DEBUG=str_to_bool(str(os.getenv('DEBUG', 1))),
        IS_SECURE_COOKIE=str_to_bool(config["BASE"]["IS_SECURE_COOKIE"]),
        BASE=Base(
            TITLE=config["BASE"]["TITLE"],
            DESCRIPTION=config["BASE"]["DESCRIPTION"],
            VERSION=__version__,
            CONTACT=Contact(
                NAME=config["CONTACT"]["NAME"],
                URL=config["CONTACT"]["URL"],
                EMAIL=config["CONTACT"]["EMAIL"]
            ),
            JWT=JWT(
                ACCESS_SECRET_KEY=config["JWT"]["ACCESS_SECRET_KEY"],
                REFRESH_SECRET_KEY=config["JWT"]["REFRESH_SECRET_KEY"]
            )
        ),
        DB=DbConfig(
            REDIS=RedisConfig(
                HOST=config["REDIS"]["HOST"],
                USERNAME=config["REDIS"]["USERNAME"],
                PASSWORD=config["REDIS"]["PASSWORD"],
                PORT=int(config["REDIS"]["PORT"])
            ) if str_to_bool(config["REDIS"]["is_used"]) else None,
        ),
    )

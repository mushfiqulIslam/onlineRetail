import os
from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL: str = os.environ.get("POSTGRES_URL", "")
    SHOW_SQL_ALCHEMY_QUERIES: int = 0
    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24


config: Config = Config()

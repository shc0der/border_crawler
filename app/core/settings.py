from functools import lru_cache
from typing import Optional, Any, Dict

from pydantic import field_validator, PostgresDsn
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str
    PROJECT_VERSION: str

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v

        return str(PostgresDsn.build(
            scheme="postgresql",
            username=info.data["POSTGRES_USER"],
            password=info.data['POSTGRES_PASSWORD'],
            host=info.data['POSTGRES_SERVER'],
            path=info.data['POSTGRES_DB'],
            port=info.data["POSTGRES_PORT"]
        ))

    BORDER_URL: str
    COOKIE_URL: str
    HEADERS: Dict[str, Any] = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    class Config:
        extra = 'allow'
        env_file = '.env'
        case_sensitive = True
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()

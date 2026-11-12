from functools import lru_cache
from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_user: str = "postgres"
    db_password: str = "CHANGE_ME"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "day19_crud_h"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> URL:
        # 비밀번호를 URL 문자열로 직접 이어 붙이지 않고 URL.create가 인코딩을 맡습니다.
        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()

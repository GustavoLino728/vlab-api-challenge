from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_url_sync: str
    api_key: str = "changeme"

    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_db: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()

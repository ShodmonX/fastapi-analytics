from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TITLE: str
    API_VERSION: str
    DEBUG: bool
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
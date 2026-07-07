from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://barquiz:barquiz@localhost:5432/barquiz"
    anthropic_api_key: str = ""
    courtlistener_api_token: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

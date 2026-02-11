from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    exito_enabled: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

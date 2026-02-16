from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Carga variables de entorno desde .env
    """

    exito_enabled: bool = False
    alkosto_enabled: bool = False
    redis_url: str = "redis://localhost:6379/0"
    mongo_url: str = "mongodb://admin:adminpassword@localhost:27017"
    mongo_db_name: str = "webscraping"
    log_level: str = "INFO"

    # Seguridad
    secret_key: str = "your-secret-key-for-development"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
    )


settings = Settings()

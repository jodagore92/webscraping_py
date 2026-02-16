from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Carga variables de entorno desde .env
    """

    exito_enabled: bool
    alkosto_enabled: bool
    redis_url: str
    mongo_url: str
    mongo_db_name: str
    log_level: str

    # Credenciales de inicialización (para consistencia con .env)
    mongo_initdb_root_username: str
    mongo_initdb_root_password: str

    # Seguridad
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
    )


settings = Settings()

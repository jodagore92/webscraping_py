import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    EXITO_ENABLED: bool = os.getenv("EXITO_ENABLED", "false").lower() == "true"


settings = Settings()

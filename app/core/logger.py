import logging
import sys
from app.core.config import settings


def setup_logger(name: str) -> logging.Logger:
    """Configuración estándar de logging para toda la aplicación."""

    logger = logging.getLogger(name)

    # Evitar duplicados si el logger ya tiene handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(settings.log_level.upper())

    # Formato de los logs
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para consola (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevenir que los logs se propaguen al root logger (evitar duplicados en FastAPI/Uvicorn)
    logger.propagate = False

    return logger


# Instancia global o helper para obtener loggers por nombre de módulo
logger = setup_logger("app")

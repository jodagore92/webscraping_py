from celery import Celery
from app.core.config import Settings

# Obtener configuración
settings = Settings()

# Crear instancia de Celery
celery_app = Celery(
    "webscraping_py",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

# Configuración de Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    result_expires=3600,  # 1 hora
)

# Importar tareas para que Celery las registre
import app.infrastructure.worker.celery_tasks  # noqa: F401, E402

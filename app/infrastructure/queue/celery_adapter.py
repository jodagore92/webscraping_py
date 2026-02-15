from typing import Any, Optional
from celery.result import AsyncResult

from app.infrastructure.queue.queue_provider import QueueProvider
from app.core.logger import logger


class CeleryAdapter(QueueProvider):
    """Adaptador de Celery para colas de tareas"""

    def __init__(self, celery_app):
        """
        Inicializa el adaptador con una app de Celery

        Args:
            celery_app: Instancia de celery.Celery
        """
        self.app = celery_app

    async def enqueue(self, task_name: str, *args, **kwargs) -> str:
        """Encola una tarea en Celery"""
        # Celery espera el nombre completo del módulo donde está la tarea
        full_task_name = f"app.infrastructure.worker.celery_tasks.{task_name}"
        result = self.app.send_task(full_task_name, args=args, kwargs=kwargs)
        logger.info(f"Tarea encolada: {full_task_name} [job_id: {result.id}]")
        return result.id

    async def get_result(self, job_id: str) -> Optional[Any]:
        """Obtiene el resultado de una tarea encolada"""
        async_result = AsyncResult(job_id, app=self.app)

        if async_result.successful():
            return async_result.result
        elif async_result.failed():
            return None
        else:
            # Aún está procesando
            return None

    async def get_status(self, job_id: str) -> str:
        """Obtiene el estado de una tarea"""
        async_result = AsyncResult(job_id, app=self.app)

        # En Celery, si el job_id no existe en el backend de resultados (expire time o nunca existió),
        # el estado devuelto es PENDING por defecto.
        # Verificamos si la tarea realmente existe o ha sido guardada.
        backend = self.app.backend
        if backend and not backend.get(backend.get_key_for_task(job_id)):
            return "unknown"

        state = async_result.state

        # Mapear estados de Celery a nuestros estados
        state_map = {
            "PENDING": "pending",
            "STARTED": "processing",
            "PROCESSING": "processing",
            "SUCCESS": "completed",
            "FAILURE": "failed",
            "RETRY": "processing",
            "REVOKED": "failed",
        }

        return state_map.get(state, "unknown")

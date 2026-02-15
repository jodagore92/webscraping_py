from typing import Any, Optional
from celery.result import AsyncResult

from app.infrastructure.queue.queue_provider import QueueProvider


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

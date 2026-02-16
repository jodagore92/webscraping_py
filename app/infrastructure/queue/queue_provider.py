from abc import ABC, abstractmethod
from typing import Any, Optional


class QueueProvider(ABC):
    """Abstracción para proveedores de colas (Celery, RQ, etc)"""

    @abstractmethod
    async def enqueue(self, task_name: str, *args, **kwargs) -> str:
        """
        Encola una tarea y retorna el job_id

        Args:
            task_name: Nombre de la tarea (ej: "search_task")
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados

        Returns:
            job_id: Identificador único de la tarea encolada
        """
        pass

    @abstractmethod
    async def get_result(self, job_id: str) -> Optional[Any]:
        """
        Obtiene el resultado de una tarea

        Args:
            job_id: Identificador de la tarea

        Returns:
            Resultado de la tarea o None si aún está procesando
        """
        pass

    @abstractmethod
    async def get_status(self, job_id: str) -> str:
        """
        Obtiene el estado de una tarea

        Returns:
            Estado: "pending", "processing", "completed", "failed"
        """
        pass

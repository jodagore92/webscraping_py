from typing import Optional

from app.infrastructure.queue.queue_provider import QueueProvider


class QueueFactory:
    """Factory para gestionar el proveedor de colas"""

    _provider: Optional[QueueProvider] = None

    @classmethod
    def init(cls, provider: QueueProvider) -> None:
        """
        Inicializa el factory con un proveedor específico

        Args:
            provider: Instancia de un QueueProvider (Celery, RQ, etc)
        """
        cls._provider = provider

    @classmethod
    def get(cls) -> QueueProvider:
        """
        Obtiene la instancia del proveedor de colas

        Returns:
            QueueProvider: El proveedor inicializado

        Raises:
            RuntimeError: Si no se ha inicializado el factory
        """
        if cls._provider is None:
            raise RuntimeError(
                "QueueFactory no ha sido inicializado. "
                "Llama a QueueFactory.init() en el startup de la aplicación."
            )
        return cls._provider

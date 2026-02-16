from app.infrastructure.queue.queue_provider import QueueProvider


class SearchProductsUseCase:
    """
    Caso de uso para encolar búsquedas de productos.
    Capa de Aplicación - Arquitectura Hexagonal.
    """

    def __init__(self, queue_provider: QueueProvider):
        self.queue_provider = queue_provider

    async def execute(self, product_query: str, user_id: str = None) -> str:
        """
        Ejecuta la lógica de encolamiento de búsqueda.
        """
        # Aquí se podría agregar validación de negocio cruzada o
        # interacción con otros puertos (ej: auditoría, caché).
        job_id = await self.queue_provider.enqueue(
            "search_task", product_query, user_id=user_id
        )
        return job_id

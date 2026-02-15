from typing import Any, Optional, Dict, Union
from app.infrastructure.queue.queue_provider import QueueProvider
from app.models.product import Product, SearchStatus, SearchResponse, StoreMetadata


class GetSearchResultUseCase:
    """
    Caso de uso para obtener el estado o resultado de una búsqueda.
    Capa de Aplicación - Arquitectura Hexagonal.
    """

    def __init__(self, queue_provider: QueueProvider):
        self.queue_provider = queue_provider

    async def execute(self, job_id: str) -> Union[SearchResponse, SearchStatus]:
        """
        Consulta la infraestructura para retornar el estado o el resultado.
        """
        result = await self.queue_provider.get_result(job_id)
        status = await self.queue_provider.get_status(job_id)

        if result is None:
            message = "La búsqueda aún está procesando"
            if status == "failed":
                message = "La búsqueda ha fallado. Revisa los logs del servidor."
            elif status == "unknown":
                message = "No se encontró el job_id especificado."

            return SearchStatus(
                job_id=job_id,
                status=status,
                message=message,
            )

        # Retornar resultados transformados a modelos de dominio/respuesta
        return SearchResponse(
            data=[Product(**product) for product in result["data"]],
            metadata=[StoreMetadata(**m) for m in result.get("metadata", [])],
            total_execution_time_seconds=result.get(
                "total_execution_time_seconds", 0.0
            ),
        )

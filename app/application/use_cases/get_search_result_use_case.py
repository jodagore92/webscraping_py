from typing import Any, Optional, Dict, Union
from fastapi import HTTPException
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
        status = await self.queue_provider.get_status(job_id)

        if status == "unknown":
            raise HTTPException(
                status_code=404, detail=f"No se encontró el job_id {job_id}."
            )

        result = await self.queue_provider.get_result(job_id)

        if result is None:
            message = "La búsqueda aún está procesando"
            if status == "failed":
                message = "La búsqueda ha fallado. Revisa los logs del servidor."

            return SearchStatus(
                job_id=job_id,
                status=status,
                message=message,
            )

        # Retornar resultados transformados a modelos de dominio/respuesta
        return SearchResponse(
            data=[Product(**product) for product in result["data"]],
            metadata=[StoreMetadata(**m) for m in result.get("metadata", [])],
            total_time=result.get("total_time", 0.0),
        )

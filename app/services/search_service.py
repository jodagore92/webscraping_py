from typing import List, Optional, Callable
import asyncio
from app.models.product import Product
from app.services.integration_resolver import IntegrationResolver


class SearchService:
    def __init__(self):
        self.providers = IntegrationResolver.get_active_providers()

    async def search(self, product: str) -> List[Product]:
        """Búsqueda pura que retorna objetos de dominio combinados"""
        tasks = [provider.search_products(product) for provider in self.providers]
        results = await asyncio.gather(*tasks)

        # Aplanar la lista de listas
        flat_results = [item for sublist in results for item in sublist]
        return flat_results

    async def search_and_format(
        self, product: str, on_progress: Optional[Callable[[int, int], None]] = None
    ) -> List[dict]:
        """
        Orquesta la búsqueda y formatea los resultados para transporte (JSON).
        Este método es agnóstico al worker (Celery, RQ, etc).
        """
        if on_progress:
            on_progress(10, 100)

        results = await self.search(product)

        if on_progress:
            on_progress(100, 100)

        # Convertir modelos Pydantic a diccionarios JSON-safe
        return [product.model_dump(mode="json") for product in results]

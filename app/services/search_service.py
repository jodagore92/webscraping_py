from typing import List, Optional, Callable, Dict, Any, Tuple
import asyncio
import time
from app.models.product import Product, StoreMetadata
from app.services.integration_resolver import IntegrationResolver


class SearchService:
    def __init__(self):
        self.providers = IntegrationResolver.get_active_providers()

    async def _search_with_metadata(
        self, provider, query: str
    ) -> Tuple[List[Product], StoreMetadata]:
        """Ejecuta la búsqueda y calcula métricas para un proveedor específico"""
        start_time = time.perf_counter()
        try:
            results = await provider.search_products(query)
        except Exception:
            results = []
        end_time = time.perf_counter()

        metadata = StoreMetadata(
            store_name=provider.__class__.__name__.replace("Scraper", ""),
            count=len(results),
            execution_time_seconds=round(end_time - start_time, 2),
        )
        return results, metadata

    async def search(self, product: str) -> Tuple[List[Product], List[StoreMetadata]]:
        """Búsqueda pura que retorna objetos de dominio combinados y metadata"""
        tasks = [self._search_with_metadata(p, product) for p in self.providers]
        combined_results = await asyncio.gather(*tasks)

        all_products = []
        all_metadata = []

        for products, meta in combined_results:
            all_products.extend(products)
            all_metadata.append(meta)

        return all_products, all_metadata

    async def search_and_format(
        self, product: str, on_progress: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Orquesta la búsqueda y formatea los resultados para transporte (JSON).
        Este método es agnóstico al worker (Celery, RQ, etc).
        """
        if on_progress:
            on_progress(10, 100)

        start_time = time.perf_counter()
        products, metadata = await self.search(product)
        end_time = time.perf_counter()

        if on_progress:
            on_progress(100, 100)

        # Convertir modelos Pydantic a diccionarios JSON-safe
        return {
            "data": [p.model_dump(mode="json") for p in products],
            "metadata": [m.model_dump(mode="json") for m in metadata],
            "total_time": round(end_time - start_time, 2),
        }

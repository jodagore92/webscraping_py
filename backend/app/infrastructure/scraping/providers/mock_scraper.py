import asyncio
from typing import List
from app.models.product import Product
from app.infrastructure.scraping.providers.base_scraper import BaseScraper, ProductData
from app.core.logger import logger


class MockScraper(BaseScraper):
    """
    Mock Scraper para testing y desarrollo.

    Retorna datos de prueba sin realizar scraping real.
    Infrastructure Layer - Mock Implementation
    """

    BASE_URL = "https://www.mockstore.com"

    def _build_search_url(self, query: str) -> str:
        """
        Construye URL ficticia para el mock.

        Args:
            query: Término de búsqueda

        Returns:
            URL mock
        """
        return f"{self.BASE_URL}/search?q={query}"

    def _extract_product_data(self, html: str) -> list[ProductData]:
        """
        Mock de extracción - no se usa en esta implementación.

        Args:
            html: Contenido HTML (no usado)

        Returns:
            Lista vacía
        """
        return []

    async def search_products(self, query: str) -> List[Product]:
        """
        Retorna productos de prueba sin realizar scraping real.

        Args:
            query: Término de búsqueda (usado en nombre de producto)

        Returns:
            Lista de productos mock
        """
        logger.info(f"[{self.__class__.__name__}] Inicio de búsqueda para: {query}")
        await asyncio.sleep(0.5)  # Simular latencia

        logger.info(f"[{self.__class__.__name__}] Organizando datos extraídos...")
        results = [
            Product(
                name=f"{query.capitalize()} Demo {i}",
                store="MockStore",
                price=100000.0,
                url=f"{self.BASE_URL}/product/{i}",
                image=f"{self.BASE_URL}/images/product-{i}.jpg",
            )
            for i in range(1, 4)
        ]
        logger.info(
            f"[{self.__class__.__name__}] Finalizado. Encontrados: {len(results)}"
        )
        return results

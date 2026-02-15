from abc import ABC, abstractmethod
from dataclasses import dataclass
from app.models.product import Product


@dataclass
class ProductData:
    """Estructura de datos para productos extraídos del HTML"""

    name: str
    store: str
    price: float
    image: str | None
    url: str | None


class BaseScraper(ABC):
    """
    Clase abstracta base para todos los scrapers de e-commerce.

    Define el contrato que deben cumplir todos los scrapers:
    - Cada scraper debe implementar search_products()
    - Cada scraper debe definir BASE_URL
    - Cada scraper debe implementar _build_search_url()

    Pattern: Template Method + Abstract Base Class

    Infrastructure Layer - Adapter Pattern
    """

    BASE_URL: str

    @abstractmethod
    def _build_search_url(self, query: str) -> str:
        """
        Construye la URL de búsqueda con el query proporcionado.

        Cada e-commerce tiene su propia estructura de URL de búsqueda.

        Args:
            query: Término de búsqueda

        Returns:
            URL completa para realizar la búsqueda
        """
        pass

    @abstractmethod
    async def search_products(self, query: str) -> list[Product]:
        """
        Busca productos en el e-commerce y retorna lista de objetos Product.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de objetos Product con la información obtenida

        Raises:
            NotImplementedError: Si el método no está implementado
        """
        pass

    @abstractmethod
    def _extract_product_data(self, html: str) -> list[ProductData]:
        """
        Extrae información de productos del HTML.

        Cada scraper debe implementar su propia lógica de extracción
        según la estructura HTML del e-commerce específico.

        Args:
            html: Contenido HTML de la página

        Returns:
            Lista de ProductData con la información extraída
        """
        pass

    def get_source_name(self) -> str:
        """
        Retorna el nombre de la fuente del scraper.

        Por defecto retorna el nombre de la clase sin 'Scraper'.
        Puede ser sobreescrito por las clases hijas.
        """
        return self.__class__.__name__.replace("Scraper", "").lower()

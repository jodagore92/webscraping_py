from abc import ABC, abstractmethod
from dataclasses import dataclass
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
from app.models.product import Product


@dataclass
class ProductData:
    """Estructura de datos para productos extraídos del HTML"""

    name: str
    price: str
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


class ExitoScraper(BaseScraper):
    BASE_URL = "https://www.exito.com"

    def _build_search_url(self, query: str) -> str:
        """
        Construye la URL de búsqueda para Éxito.

        Args:
            query: Término de búsqueda

        Returns:
            URL completa: https://www.exito.com/s?q={query}
        """
        return f"{self.BASE_URL}/s?q={query}"

    def _extract_product_data(self, html: str) -> list[ProductData]:
        """
        Extrae información de productos del HTML usando selectolax.

        Args:
            html: Contenido HTML de la página

        Returns:
            Lista de ProductData con la información extraída
        """
        parser = HTMLParser(html)
        products = []

        # Iterar sobre todos los articles
        for card in parser.css("article"):
            # Nombre
            name_elem = card.css_first("h3")
            if not name_elem:
                continue
            name = name_elem.text(strip=True)

            # Precio
            price_elem = card.css_first('p[data-fs-container-price-otros="true"]')
            price = ""
            if price_elem:
                price_text = price_elem.text(strip=True)
                price = price_text.replace("$", "").replace(".", "").strip()

            # Imagen
            img_elem = card.css_first('button[data-fs-image-zoom-container="true"] img')
            if not img_elem:
                img_elem = card.css_first("img[src*='vtexassets.com']")

            image_url = None
            if img_elem:
                image_url = img_elem.attrs.get("src")

            # URL
            link_elem = card.css_first("a")
            url = None
            if link_elem:
                relative_url = link_elem.attrs.get("href")
                if relative_url:
                    url = (
                        f"https://www.exito.com{relative_url}"
                        if relative_url.startswith("/")
                        else relative_url
                    )

            products.append(
                ProductData(name=name, price=price, image=image_url, url=url)
            )

        return products

    async def search_products(self, query: str) -> list[Product]:
        """
        Busca productos en Éxito y retorna lista de objetos Product.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de objetos Product con la información obtenida
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True  # cambiar a False para debug
            )
            context = await browser.new_context()
            page = await context.new_page()

            search_url = self._build_search_url(query)
            await page.goto(search_url, timeout=60000)
            await page.wait_for_selector("article h3", timeout=30000)
            await page.wait_for_timeout(3000)

            # Scroll para activar lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)

            # Obtener el HTML
            html = await page.content()

            # Extraer datos usando selectolax
            products_data = self._extract_product_data(html)

            # Convertir a objetos Product
            products = []
            for p in products_data:
                try:
                    product = Product(
                        name=p.name,
                        price=p.price,
                        url=p.url if p.url else self.BASE_URL,
                        image=p.image,
                    )
                    products.append(product)
                except Exception as e:
                    # Log del error pero continuar procesando
                    print(f"Error al crear Product: {e}")
                    continue

            await browser.close()

        return products

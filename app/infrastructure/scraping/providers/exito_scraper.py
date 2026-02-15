from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
from app.models.product import Product
from app.infrastructure.scraping.providers.base_scraper import BaseScraper, ProductData
from app.core.logger import logger


class ExitoScraper(BaseScraper):
    """
    Scraper para Éxito - E-commerce colombiano.

    Implementación concreta del adaptador para integración con Éxito.
    Infrastructure Layer - Adapter Pattern
    """

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
            price = 0.0
            if price_elem:
                price_text = price_elem.text(strip=True)
                price = price_text.replace("$", "").replace(".", "").strip()
                price = float(price) if price.isdigit() else 0.0

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
                ProductData(
                    name=name, store="Éxito", price=price, image=image_url, url=url
                )
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
        logger.info(f"[{self.__class__.__name__}] Inicio de búsqueda para: {query}")
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

            logger.info(f"[{self.__class__.__name__}] Organizando datos extraídos...")
            # Extraer datos usando selectolax
            products_data = self._extract_product_data(html)

            # Convertir a objetos Product
            products = []
            for p in products_data:
                try:
                    product = Product(
                        name=p.name,
                        store=p.store,
                        price=p.price,
                        url=p.url
                        if p.url
                        else self.BASE_URL,  # URL por defecto si es None
                        image=p.image,
                    )
                    products.append(product)
                except Exception as e:
                    # Log del error pero continuar procesando
                    logger.error(f"Error al crear Product: {e}")
                    continue

            await browser.close()

        logger.info(
            f"[{self.__class__.__name__}] Finalizado. Encontrados: {len(products)}"
        )
        return products

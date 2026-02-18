from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
from app.models.product import Product
from app.infrastructure.scraping.providers.base_scraper import BaseScraper, ProductData
from app.core.logger import logger


class AlkostoScraper(BaseScraper):
    """
    Scraper para Alkosto - E-commerce colombiano.

    Implementación concreta del adaptador para integración con Alkosto.
    Infrastructure Layer - Adapter Pattern
    """

    BASE_URL = "https://www.alkosto.com"

    def _build_search_url(self, query: str) -> str:
        """
        Construye la URL de búsqueda para Alkosto.

        Args:
            query: Término de búsqueda

        Returns:
            URL completa: https://www.alkosto.com/search?text={query}
        """
        return f"{self.BASE_URL}/search?text={query}"

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

        # En Alkosto los productos suelen estar en elementos li con clase product__item
        for card in parser.css("li.product__item"):
            # Nombre
            name_elem = card.css_first(
                "h3.product__item__top__title"
            ) or card.css_first("h3")
            if not name_elem:
                continue
            name = name_elem.text(strip=True)

            # Precio - Buscamos el precio actual (frecuentemente tiene clase price)
            price_elem = card.css_first("span.price") or card.css_first(
                ".product__item__information__price"
            )
            if not price_elem:
                continue

            # Limpiar precio para convertir a float
            price_text = price_elem.text(strip=True)
            # Quitar $, puntos, espacios y "Hoy" si existe
            clean_price = (
                price_text.replace("$", "")
                .replace(".", "")
                .replace("Hoy", "")
                .replace("\xa0", "")
                .strip()
            )
            try:
                price = float(clean_price)
            except ValueError:
                price = 0.0

            # Imagen
            img_elem = card.css_first("img")
            image = img_elem.attributes.get("src") if img_elem else None
            # A veces usan data-src para lazy loading
            if not image and img_elem:
                image = img_elem.attributes.get("data-src")
            
            if image and image.startswith("/"):
                image = f"{self.BASE_URL}{image}"

            # URL
            link_elem = card.css_first("a")
            url = link_elem.attributes.get("href") if link_elem else None
            if url and not url.startswith("http"):
                url = f"{self.BASE_URL}{url}"

            products.append(
                ProductData(
                    name=name, store="Alkosto", price=price, image=image, url=url
                )
            )

        return products

    async def search_products(self, query: str) -> list[Product]:
        """
        Realiza la búsqueda en Alkosto y retorna lista de Productos.
        """
        logger.info(f"[{self.__class__.__name__}] Inicio de búsqueda para: {query}")
        search_url = self._build_search_url(query)
        logger.info(f"Buscando en Alkosto: {search_url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # User agent para evitar bloqueos básicos
            await page.set_extra_http_headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                }
            )

            try:
                await page.goto(search_url, timeout=40000)
                # Esperar a que carguen los productos
                await page.wait_for_selector("li.product__item", timeout=30000)
                html = await page.content()

                logger.info(f"[{self.__class__.__name__}] Organizando datos extraídos...")
                product_datas = self._extract_product_data(html)

                results = [
                    Product(
                        name=data.name,
                        store=data.store,
                        price=data.price,
                        url=data.url,
                        image=data.image,
                    )
                    for data in product_datas
                    if data.url  # Validar que al menos tenga URL
                ]
                logger.info(
                    f"[{self.__class__.__name__}] Finalizado. Encontrados: {len(results)}"
                )
                return results

            except Exception as e:
                logger.error(f"Error raspando Alkosto: {str(e)}")
                return []
            finally:
                await browser.close()

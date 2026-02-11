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


class ExitoScraper:
    BASE_URL = "https://www.exito.com"
    SEARCH_URL = "https://www.exito.com/s?q={query}"

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

            await page.goto(self.SEARCH_URL.format(query=query), timeout=60000)
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
                        url=p.url
                        if p.url
                        else self.BASE_URL,  # URL por defecto si es None
                        image=p.image,
                    )
                    products.append(product)
                except Exception as e:
                    # Log del error pero continuar procesando
                    print(f"Error al crear Product: {e}")
                    continue

            await browser.close()

        return products

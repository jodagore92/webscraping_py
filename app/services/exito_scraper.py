from playwright.async_api import async_playwright
from app.models.product import Product


class ExitoScraper:

    BASE_URL = "https://www.exito.com"
    SEARCH_URL = "https://www.exito.com/s?q={query}"

    async def search_products(self, query: str) -> list[Product]:
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True  # cambiar a False para debug
            )
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()

            await page.goto(self.SEARCH_URL.format(query=query), timeout=60000)
            await page.wait_for_selector("article h3", timeout=30000)
            await page.wait_for_timeout(3000)

            # Scroll para activar lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)

            cards = page.locator("article").filter(
                has=page.locator("h3")
            )

            results = []

            count = await cards.count()

            for i in range(count):
                card = cards.nth(i)
                name = await card.locator("h3").first.inner_text()

                # Precio
                price_locator = card.locator('p[data-fs-container-price-otros="true"]')
                if await price_locator.count() > 0:
                    price_text = await price_locator.inner_text()
                    price = price_text.replace("$", "").replace(".", "").strip()
                else:
                    price = ""

                # Imagen
                img_locator = card.locator(
                    'button[data-fs-image-zoom-container="true"] img'
                )

                if await img_locator.count() == 0:
                    img_locator = card.locator("img[src*='vtexassets.com']")

                image_url = (
                    await img_locator.first.get_attribute("src")
                    if await img_locator.count() > 0
                    else None
                )

                relative_url = await card.locator("a").first.get_attribute("href")

                url = (
                    f"https://www.exito.com{relative_url}"
                    if relative_url and relative_url.startswith("/")
                    else relative_url
                )

                results.append({
                    "name": name,
                    "price": price,
                    "image": image_url,
                    "url":url
                })

            await browser.close()

        return results

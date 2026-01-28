from typing import List
from app.models.product import Product


class ExitoScraper:

    async def search_products(self, product: str) -> List[Product]:
        # Aquí irá Playwright real
        return [
            Product(
                name=f"Licuadora real {i}",
                price="$200.000",
                url="https://www.exito.com",
                image=None
            )
            for i in range(1, 4)
        ]

from typing import List
from app.models.product import Product


class MockProductsProvider:

    async def search_products(self, product: str) -> List[Product]:
        return [
            Product(
                name=f"Licuadora demo {i}",
                price="$100.000",
                url="https://www.algunemcommerce.com/demo",
                image=None
            )
            for i in range(1, 4)
        ]

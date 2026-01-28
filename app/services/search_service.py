from typing import List
from app.models.product import Product
from app.services.integration_resolver import IntegrationResolver


class SearchService:

    def __init__(self):
        self.provider = IntegrationResolver.get_exito_provider()

    async def search(self, product: str) -> List[Product]:
        return await self.provider.search_products(product)

from app.core.config import settings
from app.services.exito_scraper import ExitoScraper
from app.services.mock_products_provider import MockProductsProvider


class IntegrationResolver:

    @staticmethod
    def get_exito_provider():
        if settings.EXITO_ENABLED:
            return ExitoScraper()
        return MockProductsProvider()

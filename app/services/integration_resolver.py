from app.core.config import settings
from app.infrastructure.scraping.providers import (
    ExitoScraper,
    AlkostoScraper,
    MockScraper,
)


class IntegrationResolver:
    """
    Factory para resolver qué scraper utilizar según configuración.

    Factory Pattern - Infrastructure Layer
    """

    @staticmethod
    def get_exito_provider():
        """
        Retorna el scraper apropiado según configuración.

        Returns:
            ExitoScraper si está habilitado, MockScraper en caso contrario
        """
        if settings.exito_enabled:
            return ExitoScraper()
        return MockScraper()

    @staticmethod
    def get_alkosto_provider():
        """
        Retorna el scraper de Alkosto si está habilitado.
        """
        if settings.alkosto_enabled:
            return AlkostoScraper()
        return None

    @staticmethod
    def get_active_providers():
        """
        Retorna una lista de todos los scrapers habilitados.
        """
        providers = []
        if settings.exito_enabled:
            providers.append(ExitoScraper())
        if settings.alkosto_enabled:
            providers.append(AlkostoScraper())

        # Si no hay ninguno habilitado, devolvemos el Mock por defecto
        if not providers:
            providers.append(MockScraper())

        return providers

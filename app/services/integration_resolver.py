from app.core.config import settings
from app.infrastructure.scraping.providers import ExitoScraper, MockScraper


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

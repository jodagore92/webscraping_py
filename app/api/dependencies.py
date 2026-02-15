from app.services.queue_factory import QueueFactory
from app.application.use_cases.search_products_use_case import SearchProductsUseCase
from app.application.use_cases.get_search_result_use_case import GetSearchResultUseCase


def get_search_products_use_case() -> SearchProductsUseCase:
    """Inyecta el caso de uso de búsqueda con su infraestructura"""
    queue_provider = QueueFactory.get()
    return SearchProductsUseCase(queue_provider)


def get_search_result_use_case() -> GetSearchResultUseCase:
    """Inyecta el caso de uso de obtención de resultados"""
    queue_provider = QueueFactory.get()
    return GetSearchResultUseCase(queue_provider)

"""Scraping Providers - Implementaciones concretas de scrapers"""

from app.infrastructure.scraping.providers.base_scraper import BaseScraper, ProductData
from app.infrastructure.scraping.providers.exito_scraper import ExitoScraper
from app.infrastructure.scraping.providers.alkosto_scraper import AlkostoScraper
from app.infrastructure.scraping.providers.mock_scraper import MockScraper

__all__ = [
    "BaseScraper",
    "ProductData",
    "ExitoScraper",
    "AlkostoScraper",
    "MockScraper",
]

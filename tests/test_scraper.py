import asyncio
from app.services.exito_scraper import ExitoScraper

async def test():
    scraper = ExitoScraper()
    products = await scraper.search("licuadora")
    print(products)

asyncio.run(test())

from fastapi import APIRouter, Query
from typing import List

from app.models.product import Product
from app.services.search_service import SearchService

router = APIRouter(tags=["Search"])
service = SearchService()


@router.get("/search", response_model=List[Product])
async def search_product(
    product: str = Query(..., min_length=2)
):
    return await service.search(product)

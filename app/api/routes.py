from fastapi import APIRouter, Query, Depends
from typing import Union

from app.models.product import SearchStatus, SearchResponse
from app.models.user import UserInDB
from app.api.dependencies import (
    get_search_products_use_case,
    get_search_result_use_case,
    get_current_user,
)
from app.application.use_cases.search_products_use_case import SearchProductsUseCase
from app.application.use_cases.get_search_result_use_case import GetSearchResultUseCase

router = APIRouter(tags=["Search"])


@router.post("/search")
async def search_product(
    product: str = Query(..., min_length=2),
    use_case: SearchProductsUseCase = Depends(get_search_products_use_case),
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Encola una búsqueda de productos via Use Case
    """
    job_id = await use_case.execute(product, user_id=current_user.id)
    return {
        "job_id": job_id,
        "status_url": f"/api/search/{job_id}",
        "message": "Búsqueda encolada. Consulta el resultado con el job_id",
    }


@router.get("/search/{job_id}", response_model=Union[SearchResponse, SearchStatus])
async def get_search_result(
    job_id: str,
    use_case: GetSearchResultUseCase = Depends(get_search_result_use_case),
    current_user: UserInDB = Depends(get_current_user),
):
    """
    Obtiene el resultado de una búsqueda encolada via Use Case
    """
    # Nota: Aquí podríamos validar que el job_id pertenezca al current_user
    # consultando la base de datos si el status es SUCCESS.
    return await use_case.execute(job_id)

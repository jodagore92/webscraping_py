from fastapi import APIRouter, Depends
from typing import List
from app.application.use_cases.get_history import GetSearchHistoryUseCase
from app.api.dependencies import get_history_use_case, get_current_user
from app.models.user import UserInDB

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/history")
async def get_my_history(
    limit: int = 10,
    skip: int = 0,
    current_user: UserInDB = Depends(get_current_user),
    use_case: GetSearchHistoryUseCase = Depends(get_history_use_case),
):
    """
    Retorna el historial de búsquedas del usuario autenticado con paginación.
    """
    history = await use_case.execute(current_user.id, limit=limit, skip=skip)
    return history

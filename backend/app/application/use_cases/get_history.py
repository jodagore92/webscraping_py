from typing import List
from app.infrastructure.database.database_provider import DatabaseProvider


class GetSearchHistoryUseCase:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    async def execute(self, user_id: str, limit: int = 10, skip: int = 0) -> List[dict]:
        return await self.db.list_user_searches(user_id, limit=limit, skip=skip)

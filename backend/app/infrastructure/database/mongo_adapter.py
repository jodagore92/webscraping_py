from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.infrastructure.database.database_provider import DatabaseProvider
from app.core.config import settings
from app.core.logger import logger


class MongoAdapter(DatabaseProvider):
    """
    Adaptador de MongoDB para persistencia de datos.
    """

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self._loop = None
        self.collection_name = "search_results"
        self.users_collection = "users"

    async def connect(self):
        import asyncio

        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            return

        # Si el loop cambió, reiniciamos el cliente de Motor
        if self.client is not None and self._loop != current_loop:
            logger.info(
                "Cambio de Event Loop detectado. Reiniciando cliente de MongoDB."
            )
            self.client = None
            self.db = None

        if self.client is None:
            logger.info(f"Conectando a MongoDB en: {settings.mongo_url}")
            self.client = AsyncIOMotorClient(settings.mongo_url)
            self.db = self.client[settings.mongo_db_name]
            self._loop = current_loop

            try:
                await self.db[self.users_collection].create_index("email", unique=True)
            except Exception as e:
                logger.warning(f"No se pudo crear el índice: {e}")

    async def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self._loop = None
            logger.info("Conexión cerrada con MongoDB")

    async def save_search_result(self, job_id: str, data: dict):
        await self.connect()
        await self.db[self.collection_name].update_one(
            {"job_id": job_id}, {"$set": data}, upsert=True
        )
        logger.info(f"Resultado de búsqueda guardado para job_id: {job_id}")

    async def get_search_result(self, job_id: str) -> Optional[dict]:
        await self.connect()
        return await self.db[self.collection_name].find_one({"job_id": job_id})

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        await self.connect()
        return await self.db[self.users_collection].find_one({"email": email})

    async def save_user(self, user_data: dict) -> str:
        await self.connect()
        result = await self.db[self.users_collection].insert_one(user_data)
        return str(result.inserted_id)

    async def list_user_searches(
        self, user_id: str, limit: int = 10, skip: int = 0
    ) -> list[dict]:
        await self.connect()
        cursor = (
            self.db[self.collection_name]
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .skip(skip)
        )
        results = await cursor.to_list(length=limit)
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        return results

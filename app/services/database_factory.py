from app.infrastructure.database.database_provider import DatabaseProvider
from app.infrastructure.database.mongo_adapter import MongoAdapter


class DatabaseFactory:
    """
    Factory para obtener el adaptador de base de datos configurado.
    """

    _instance: DatabaseProvider = None

    @classmethod
    def get_database(cls) -> DatabaseProvider:
        if cls._instance is None:
            # Por ahora solo soportamos MongoDB, pero aquí se podría
            # elegir basándose en la configuración
            cls._instance = MongoAdapter()
        return cls._instance

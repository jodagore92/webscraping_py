from abc import ABC, abstractmethod
from typing import Any, List, Optional


class DatabaseProvider(ABC):
    """
    Interface (Port) para proveedores de base de datos.
    Sigue el patrón Adapter para permitir cambiar de motor de BD.
    """

    @abstractmethod
    async def connect(self):
        """Establece la conexión con la base de datos."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Cierra la conexión con la base de datos."""
        pass

    @abstractmethod
    async def save_search_result(self, job_id: str, data: dict):
        """Guarda el resultado de una búsqueda."""
        pass

    @abstractmethod
    async def get_search_result(self, job_id: str) -> Optional[dict]:
        """Obtiene el resultado de una búsqueda por job_id."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Obtiene un usuario por su email."""
        pass

    @abstractmethod
    async def save_user(self, user_data: dict) -> str:
        """Guarda un nuevo usuario."""
        pass

    @abstractmethod
    async def list_user_searches(
        self, user_id: str, limit: int = 10, skip: int = 0
    ) -> List[dict]:
        """Lista el historial de búsquedas de un usuario con paginación."""
        pass

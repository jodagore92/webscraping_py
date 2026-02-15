from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class Product(BaseModel):
    name: str
    store: str
    price: float
    url: HttpUrl
    image: Optional[HttpUrl] = None


class SearchStatus(BaseModel):
    """Respuesta cuando la búsqueda aún está procesando"""

    job_id: str
    status: str
    message: str
    data: None = None
    metadata: Optional[List[dict]] = None


class StoreMetadata(BaseModel):
    store_name: str
    count: int
    execution_time_seconds: float


class SearchResponse(BaseModel):
    """Respuesta de búsqueda completada con lista de productos"""

    data: List[Product]
    metadata: List[StoreMetadata] = []
    total_execution_time_seconds: float = 0.0

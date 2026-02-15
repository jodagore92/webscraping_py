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


class SearchResponse(BaseModel):
    """Respuesta de búsqueda completada con lista de productos"""

    data: List[Product]

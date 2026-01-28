from pydantic import BaseModel, HttpUrl
from typing import Optional


class Product(BaseModel):
    name: str
    price: str
    url: HttpUrl
    image: Optional[HttpUrl] = None

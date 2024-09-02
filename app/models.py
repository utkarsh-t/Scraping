from pydantic import BaseModel, HttpUrl
from typing import Optional

class ScrapeRequest(BaseModel):
    pages_limit: Optional[int] = None
    proxy: Optional[str] = None

class ScrapedProduct(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeResponse(BaseModel):
    status: str
    message: str

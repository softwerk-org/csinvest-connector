from datetime import datetime
from pydantic import BaseModel


class PricesItem(BaseModel):
    market_hash_name: str
    volume: int
    price: float


class Prices(BaseModel):
    success: bool
    time: datetime
    currency: str
    items: list[PricesItem]

from datetime import datetime
from pydantic import BaseModel


class Sale(BaseModel):
    time: datetime
    price: float


class ResponseItem(BaseModel):
    name: str
    appid: int
    sales: list[Sale]


class SalesHistoryMulti(BaseModel):
    success: bool
    response: list[ResponseItem]

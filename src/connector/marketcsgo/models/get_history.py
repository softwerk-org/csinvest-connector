from datetime import datetime
from pydantic import BaseModel


class HistoryItem(BaseModel):
    price: float
    time: datetime
    count: int
    currency: str


class HistoryData(BaseModel):
    history: list[HistoryItem]


class HistoryResponse(BaseModel):
    data: HistoryData

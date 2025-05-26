from datetime import date
from typing import Any, List
from pydantic import BaseModel


class HistoryEntry(BaseModel):
    date: date
    priceAvg: float
    volume: int


class SalesHistory(BaseModel):
    market_stats_product: List[HistoryEntry]


class SalesHistoryResponse(BaseModel):
    data: SalesHistory
    errors: List[Any] | None = None

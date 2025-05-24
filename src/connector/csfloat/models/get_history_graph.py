from __future__ import annotations
from pydantic import TypeAdapter, BaseModel
from datetime import datetime

class HistoryGraphEntry(BaseModel):
    count: int
    day: datetime
    avg_price: float

HistoryGraph = TypeAdapter(list[HistoryGraphEntry]) 
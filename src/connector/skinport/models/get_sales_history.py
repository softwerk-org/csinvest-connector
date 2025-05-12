from typing import List, Optional
from pydantic import BaseModel, RootModel


class PeriodStats(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    avg: Optional[float] = None
    median: Optional[float] = None
    volume: Optional[int] = None


class SalesItem(BaseModel):
    market_hash_name: Optional[str] = None
    version: Optional[str] = None
    currency: Optional[str] = None
    item_page: Optional[str] = None
    market_page: Optional[str] = None
    last_24_hours: PeriodStats
    last_7_days: PeriodStats
    last_30_days: PeriodStats
    last_90_days: PeriodStats


class SalesStats(RootModel[List[SalesItem]]):
    pass

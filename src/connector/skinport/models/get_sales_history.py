from pydantic import BaseModel, RootModel


class PeriodStats(BaseModel):
    min: float | None = None
    max: float | None = None
    avg: float | None = None
    median: float | None = None
    volume: int | None = None


class SalesItem(BaseModel):
    market_hash_name: str | None = None
    version: str | None = None
    currency: str | None = None
    item_page: str | None = None
    market_page: str | None = None
    last_24_hours: PeriodStats
    last_7_days: PeriodStats
    last_30_days: PeriodStats
    last_90_days: PeriodStats


class SalesHistory(RootModel[list[SalesItem]]):
    pass

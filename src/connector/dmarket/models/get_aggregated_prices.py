from typing import List, Optional

from pydantic import BaseModel


class BestPrice(BaseModel):
    BestPrice: Optional[str] = None
    Count: Optional[float] = None

class AggregatedPrice(BaseModel):
    MarketHashName: Optional[str] = None
    Offers: Optional[BestPrice] = None
    Orders: Optional[BestPrice] = None

class GetAggregatedPrices(BaseModel):
    Error: Optional[str] = None
    Total: Optional[float] = None
    AggregatedTitles: Optional[List[AggregatedPrice]] = None


from typing import List, Optional

from pydantic import BaseModel, Field


class BestPrice(BaseModel):
    best_price: Optional[str] = Field(None, alias="BestPrice")
    count: Optional[float] = Field(None, alias="Count")

class AggregatedPrice(BaseModel):
    market_hash_name: Optional[str] = Field(None, alias='MarketHashName')
    offers: Optional[BestPrice] = Field(None, alias="Offers")
    orders: Optional[BestPrice] = Field(None, alias="Orders")

class GetAggregatedPrices(BaseModel):
    error: Optional[str] = Field(None, alias="Error")
    total: Optional[float] = Field(None, alias="Total")
    aggregated_titles: Optional[List[AggregatedPrice]] = Field(None, alias="AggregatedTitles")


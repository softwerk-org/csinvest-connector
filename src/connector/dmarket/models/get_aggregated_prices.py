from pydantic import BaseModel, Field


class BestPrice(BaseModel):
    best_price: float = Field(..., alias="BestPrice")
    count: int = Field(..., alias="Count")


class AggregatedPrice(BaseModel):
    market_hash_name: str = Field(..., alias="MarketHashName")
    offers: BestPrice = Field(..., alias="Offers")
    orders: BestPrice = Field(..., alias="Orders")


class AggregatedPrices(BaseModel):
    error: str | None = Field(None, alias="Error")
    total: int = Field(..., alias="Total")
    aggregated_titles: list[AggregatedPrice] = Field(..., alias="AggregatedTitles")

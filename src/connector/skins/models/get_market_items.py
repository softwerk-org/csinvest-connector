from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    type: Optional[str] = None
    color: Optional[str] = None
    effect: Optional[str] = None
    finish: Optional[Optional[int]] = None
    rarity: Optional[str] = None
    pattern: Optional[Optional[int]] = None
    category: Optional[str] = None
    tournament: Optional[str] = None
    description: Optional[str] = None
    weapon: Optional[str] = None
    exterior: Optional[str] = None
    max_float: Optional[float] = Field(None, alias="maxFloat")
    min_float: Optional[float] = Field(None, alias="minFloat")
    exteriors: Optional[List[str]] = None
    is_souvenir: Optional[bool] = Field(None, alias="isSouvenir")
    is_stat_trak: Optional[bool] = Field(None, alias="isStatTrak")
    phase: Optional[str] = None


class Data(BaseModel):
    slug: str
    name: str
    market_hash_name: str = Field(..., alias="marketHashName")
    game: str
    lowest_price: float = Field(..., alias="lowestPrice")
    market_price: float = Field(..., alias="marketPrice")
    currency: str
    icon_url: str = Field(..., alias="iconUrl")
    offer_count: int = Field(..., alias="offerCount")
    metadata: Metadata


class Pagination(BaseModel):
    page: int
    limit: int
    count: int
    total_pages: int = Field(..., alias="totalPages")
    total_offers: int = Field(..., alias="totalOffers")


class MarketItems(BaseModel):
    success: bool
    data: List[Data]
    pagination: Pagination

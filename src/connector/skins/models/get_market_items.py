from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    color: str
    finish: Optional[Optional[int]] = None
    rarity: str
    weapon: Optional[str] = None
    pattern: Optional[Optional[int]] = None
    category: str
    exterior: Optional[str] = None
    maxFloat: Optional[float] = None
    minFloat: Optional[float] = None
    exteriors: Optional[List[str]] = None
    description: str
    phase: Optional[str] = None
    isStatTrak: Optional[bool] = None
    type: Optional[str] = None
    effect: Optional[str] = None
    tournament: Optional[str] = None
    isSouvenir: Optional[bool] = None


class Datum(BaseModel):
    slug: str
    name: str
    marketHashName: str
    game: str
    lowestPrice: float
    marketPrice: float
    currency: str
    iconUrl: str
    offerCount: int
    metadata: Metadata


class Pagination(BaseModel):
    page: int
    limit: int
    count: int
    totalPages: int
    totalOffers: int


class MarketItems(BaseModel):
    success: bool
    data: List[Datum]
    pagination: Pagination

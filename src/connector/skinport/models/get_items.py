from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, RootModel


class ItemsItem(BaseModel):
    market_hash_name: str
    currency: str
    suggested_price: float | None = None
    item_page: str
    market_page: str
    min_price: float | None = None
    max_price: float | None = None
    mean_price: float | None = None
    median_price: float | None = None
    quantity: int
    created_at: datetime
    updated_at: datetime


class Items(RootModel[list[ItemsItem]]):
    root: list[ItemsItem]

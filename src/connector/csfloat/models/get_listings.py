from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class SellerStatistics(BaseModel):
    median_trade_time: int
    total_failed_trades: int
    total_trades: int
    total_verified_trades: int


class Seller(BaseModel):
    avatar: str | None = None
    flags: int
    online: bool
    stall_public: bool
    statistics: SellerStatistics
    steam_id: str | None = None
    username: str | None = None


class StickerScm(BaseModel):
    price: float
    volume: int


class ItemSticker(BaseModel):
    stickerId: int
    slot: int
    icon_url: str
    name: str
    scm: StickerScm | None = None


class ItemScm(BaseModel):
    price: float
    volume: int


class ListingItem(BaseModel):
    asset_id: str
    def_index: int
    paint_index: int | None = None
    paint_seed: int | None = None
    float_value: float | None = None
    icon_url: str
    d_param: str | None = None
    is_stattrak: bool | None = None
    is_souvenir: bool | None = None
    rarity: int
    quality: int | None = None
    market_hash_name: str
    stickers: list[ItemSticker] = Field(default_factory=list)
    tradable: int
    inspect_link: str | None = None
    has_screenshot: bool | None = None
    scm: ItemScm | None = None
    item_name: str
    wear_name: str | None = None
    description: str | None = None
    collection: str | None = None
    badges: list[Any] = Field(default_factory=list)


class Listing(BaseModel):
    id: str
    created_at: datetime
    type: str
    price: float
    state: str
    seller: Seller
    item: ListingItem
    is_seller: bool
    min_offer_price: int | None = None
    max_offer_discount: int | None = None
    is_watchlisted: bool
    watchers: int


class Listings(BaseModel):
    data: list[Listing]

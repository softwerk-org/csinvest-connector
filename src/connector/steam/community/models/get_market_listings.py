from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel


class Action(BaseModel):
    link: str
    name: str


class ListingInfoAsset(BaseModel):
    currency: int
    appid: int
    contextid: str
    id: str
    amount: str
    market_actions: List[Action]


class ListingInfoItem(BaseModel):
    listingid: str
    price: int
    fee: int
    publisher_fee_app: int
    publisher_fee_percent: str
    currencyid: int
    steam_fee: int
    publisher_fee: int
    converted_price: int
    converted_fee: int
    converted_currencyid: int
    converted_steam_fee: int
    converted_publisher_fee: int
    converted_price_per_unit: int
    converted_fee_per_unit: int
    converted_steam_fee_per_unit: int
    converted_publisher_fee_per_unit: int
    asset: ListingInfoAsset


class Description(BaseModel):
    type: str
    name: str
    value: str
    color: str | None = None


class Asset(BaseModel):
    currency: int
    appid: int
    contextid: str
    id: str
    classid: str
    instanceid: str
    amount: str
    status: int
    original_amount: str
    unowned_id: str
    unowned_contextid: str
    background_color: str
    icon_url: str
    descriptions: List[Description]
    tradable: int
    actions: List[Action]
    name: str
    name_color: str
    type: str
    market_name: str
    market_hash_name: str
    market_actions: List[Action]
    commodity: int
    market_tradable_restriction: int
    market_marketable_restriction: int
    marketable: int
    app_icon: str
    owner: int


class AppDataItem(BaseModel):
    appid: int
    name: str
    icon: str


class MarketListings(BaseModel):
    success: bool
    start: int
    pagesize: int
    total_count: int
    results_html: str
    listinginfo: Dict[str, Any]
    assets: Dict[str, Any]
    currency: List[Any]
    hovers: str
    app_data: Dict[str, Any]

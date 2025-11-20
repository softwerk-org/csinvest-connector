from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Exterior(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Quality(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Rarity(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Type(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Weapon(BaseModel):
    category: str
    id: Optional[int] = None
    internal_name: str
    localized_name: str


class Tags(BaseModel):
    category: Optional[Category] = None
    exterior: Optional[Exterior] = None
    quality: Optional[Quality] = None
    rarity: Optional[Rarity] = None
    type: Optional[Type] = None
    weapon: Optional[Weapon] = None


class Info(BaseModel):
    tags: Tags


class GoodsInfo(BaseModel):
    icon_url: str
    info: Info
    item_id: Any
    original_icon_url: str
    steam_price: str
    steam_price_cny: str


class Item(BaseModel):
    appid: int
    auction_num: int
    bookmarked: bool
    buy_max_price: str
    buy_num: int
    can_bargain: bool
    can_search_by_tournament: bool
    description: Any
    game: str
    goods_info: GoodsInfo
    has_buff_price_history: bool
    id: int
    is_charm: bool
    keychain_color_img: Any
    market_hash_name: str
    market_min_price: str
    min_rent_unit_price: str
    min_security_price: str
    name: str
    pre_sell_min_price: str
    pre_sell_num: int
    quick_price: str
    rent_num: int
    rent_unit_reference_price: str
    sell_min_price: str
    sell_num: int
    sell_reference_price: str
    short_name: str
    steam_market_url: str
    transacted_num: int


class Data(BaseModel):
    items: List[Item]
    page_num: int
    page_size: int
    total_count: int
    total_page: int


class MarketGoods(BaseModel):
    code: str
    data: Data
    msg: Any

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Quality(BaseModel):
    id: int
    category: str
    internal_name: str
    localized_name: str


class Rarity(BaseModel):
    id: int
    category: str
    internal_name: str
    localized_name: str


class Type(BaseModel):
    id: int
    category: str
    internal_name: str
    localized_name: str


class Category(BaseModel):
    id: int
    category: str
    internal_name: str
    localized_name: str


class Exterior(BaseModel):
    id: int
    category: str
    internal_name: str
    localized_name: str


class Weapon(BaseModel):
    id: Optional[int] = None
    category: str
    internal_name: str
    localized_name: str


class Tags(BaseModel):
    quality: Quality
    rarity: Rarity
    type: Type
    category: Category
    exterior: Optional[Exterior] = None
    weapon: Optional[Weapon] = None


class Info(BaseModel):
    tags: Tags


class GoodsInfo(BaseModel):
    icon_url: str
    steam_price: str
    item_id: Any
    info: Info
    steam_price_cny: str
    original_icon_url: str


class Item(BaseModel):
    appid: int
    game: str
    id: int
    name: str
    market_hash_name: str
    steam_market_url: str
    sell_reference_price: str
    sell_min_price: str
    buy_max_price: str
    sell_num: int
    buy_num: int
    transacted_num: int
    goods_info: GoodsInfo
    quick_price: str
    market_min_price: str
    description: Any
    can_search_by_tournament: bool
    short_name: str
    can_bargain: bool
    rent_unit_reference_price: str
    rent_num: int
    min_rent_unit_price: str
    min_security_price: str
    is_charm: bool
    keychain_color_img: Optional[str]
    auction_num: int
    pre_sell_num: int
    pre_sell_min_price: str
    has_buff_price_history: bool
    bookmarked: bool


class Data(BaseModel):
    page_num: int
    page_size: int
    total_page: int
    total_count: int
    items: List[Item]


class MarketGoods(BaseModel):
    code: str
    data: Data
    msg: Any

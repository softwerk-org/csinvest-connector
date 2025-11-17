from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Datum(BaseModel):
    id: int
    is_favorite: Any = Field(..., alias="isFavorite")
    game_id: int = Field(..., alias="gameId")
    game_name: str = Field(..., alias="gameName")
    game_icon: str = Field(..., alias="gameIcon")
    commodity_name: str = Field(..., alias="commodityName")
    commodity_hash_name: str = Field(..., alias="commodityHashName")
    icon_url: str = Field(..., alias="iconUrl")
    icon_url_large: str = Field(..., alias="iconUrlLarge")
    on_sale_count: int = Field(..., alias="onSaleCount")
    on_lease_count: int = Field(..., alias="onLeaseCount")
    lease_unit_price: str = Field(..., alias="leaseUnitPrice")
    long_lease_unit_price: str = Field(..., alias="longLeaseUnitPrice")
    lease_deposit: str = Field(..., alias="leaseDeposit")
    price: str
    steam_price: str = Field(..., alias="steamPrice")
    steam_usd_price: str = Field(..., alias="steamUsdPrice")
    type_name: str = Field(..., alias="typeName")
    exterior: Optional[str]
    exterior_color: str = Field(..., alias="exteriorColor")
    rarity: str
    rarity_color: str = Field(..., alias="rarityColor")
    quality: Any
    quality_color: Any = Field(..., alias="qualityColor")
    sort_id: int = Field(..., alias="sortId")
    have_lease: int = Field(..., alias="haveLease")
    stickers_is_sort: bool = Field(..., alias="stickersIsSort")
    subsidy_purchase: int = Field(..., alias="subsidyPurchase")
    stickers: Any
    label: Any
    rent: str
    min_lease_deposit: Any = Field(..., alias="minLeaseDeposit")
    list_type: int = Field(..., alias="listType")
    template_purchase_count_text: Any = Field(..., alias="templatePurchaseCountText")
    template_tags: Any = Field(..., alias="templateTags")


class MarketGoods(BaseModel):
    code: int = Field(..., alias="Code")
    msg: str = Field(..., alias="Msg")
    data: List[Datum] = Field(..., alias="Data")
    total_count: int = Field(..., alias="TotalCount")

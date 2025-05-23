# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2025-05-09T20:58:27+00:00

from __future__ import annotations


from pydantic import BaseModel, Field


class BestDealsBestDealSticker(BaseModel):
    localized_name: str | None = Field(None, alias="localizedName")
    image_url: str | None = Field(None, alias="imageUrl")


class BestDealsBestDeal(BaseModel):
    sales_id: str | None = Field(None, alias="salesId")
    item_name: str | None = Field(None, alias="itemName")
    rarity_name: str | None = Field(None, alias="rarityName")
    exterior_name: str | None = Field(None, alias="exteriorName")
    variant_type_name: str | None = Field(None, alias="variantTypeName")
    is_souvenir: bool | None = Field(None, alias="isSouvenir")
    item_price: float | None = Field(None, alias="itemPrice")
    wear: float | None = None
    is_wear_precise: bool | None = Field(None, alias="isWearPrecise")
    stackable: bool | None = None
    stickers: list[BestDealsBestDealSticker | None] | None = None
    app_id: int | None = Field(None, alias="appId")
    trade_lock_hours_left: int | None = Field(None, alias="tradeLockHoursLeft")


class BestDeals(BaseModel):
    best_deals: list[BestDealsBestDeal | None] | None = Field(None, alias="bestDeals")

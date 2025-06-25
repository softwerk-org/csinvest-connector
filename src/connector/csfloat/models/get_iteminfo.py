from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class Sticker(BaseModel):
    slot: int | None = None
    sticker_id: int | None = Field(None, alias="sticker_id")
    wear: float | None = None


class ItemInfo(BaseModel):
    accountid: str | None = None
    defindex: int | None = None
    paintindex: int | None = None
    rarity: int | None = None
    quality: int | None = None
    paintseed: int | None = None
    paintwear: float | None = None
    floatvalue: float | None = None
    origin: int | None = None
    itemid: str | None = None
    stickers: list[Sticker] | None = None


class ItemInfoResponse(BaseModel):
    time: int | None = None
    url: str | None = None
    iteminfo: ItemInfo | None = None
    status: Any | None = None  # Optional field sometimes present

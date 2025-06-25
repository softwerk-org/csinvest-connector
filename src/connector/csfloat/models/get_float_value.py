from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class Sticker(BaseModel):
    slot: int | None = None
    sticker_id: int | None = Field(None, alias="sticker_id")
    wear: float | None = None


class ItemInfo(BaseModel):
    accountid: str | None = None
    defindex: str | None = None
    paintindex: str | None = None
    rarity: str | None = None
    quality: str | None = None
    paintseed: str | None = None
    paintwear: float | str | None = None
    floatvalue: float | str | None = None
    origin: str | None = None
    itemid: str | None = None
    stickers: list[Sticker] | None = None


class FloatValueResponse(BaseModel):
    time: int | None = None
    url: str | None = None
    iteminfo: ItemInfo | None = None
    status: Any | None = None  # Optional field sometimes present

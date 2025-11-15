import re
from pydantic import BaseModel, field_validator


class PriceOverview(BaseModel):
    success: bool
    lowest_price: float | None = None  # current lowest sale price
    median_price: float | None = None  # current median buy price
    volume: int | None = None  # 24 hour sale volume

    @field_validator("lowest_price", "median_price", mode="before")
    def parse_price(cls, v):
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            # remove everything except digits, dot and comma
            s = re.sub(r"[^\d.,-]", "", s)
            # our convention: dot = thousands, comma = decimal
            s = s.replace(".", "").replace(",", ".")
            return float(s)
        raise TypeError("Invalid price format")

    @field_validator("volume", mode="before")
    def parse_volume(cls, v):
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            v = v.replace(",", "")
            return int(v)
        raise TypeError("Invalid volume format")

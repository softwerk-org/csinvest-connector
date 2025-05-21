from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, model_validator


class Price(BaseModel):
    timestamp: datetime
    price: float
    volume: int

    @model_validator(mode="before")
    @classmethod
    def _parse_row(cls, v):
        if isinstance(v, list):
            ts, price, vol = v
            mon, day, year, hour_colon, offset_str = ts.split()
            month = datetime.strptime(mon, "%b").month
            hour = int(hour_colon.rstrip(":"))
            offset = int(offset_str)
            tz = timezone(timedelta(hours=offset))
            dt = datetime(int(year), month, int(day), hour, tzinfo=tz)
            return {"timestamp": dt, "price": price, "volume": vol}
        return v


class Pricehistory(BaseModel):
    success: bool
    price_prefix: str
    price_suffix: str
    prices: list[Price]

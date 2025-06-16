from datetime import datetime
from pydantic import BaseModel


class PriceTraderValue(BaseModel):
    price_trader_new: float
    time: datetime


class PriceTraderLogItem(BaseModel):
    name_id: int
    values: list[PriceTraderValue]


class PriceTraderLogData(BaseModel):
    price_trader_log: list[PriceTraderLogItem]


class PriceTraderLogResponse(BaseModel):
    data: PriceTraderLogData

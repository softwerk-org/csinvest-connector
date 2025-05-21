from datetime import datetime
from pydantic import BaseModel, field_validator


class HistoryItem(BaseModel):
    timestamp: datetime
    price: float


class ItemStats(BaseModel):
    max: float
    min: float
    average: float
    history: list[HistoryItem]

    @field_validator("history", mode="before")
    @classmethod
    def convert_history(cls, v):
        return [{"timestamp": entry[0], "price": entry[1]} for entry in v]


class listItemsInfo(BaseModel):
    success: bool
    currency: str
    data: dict[str, ItemStats]

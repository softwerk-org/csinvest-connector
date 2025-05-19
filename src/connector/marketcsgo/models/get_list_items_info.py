from datetime import datetime
from pydantic import BaseModel


class ItemStats(BaseModel):
    max: float
    min: float
    average: float
    history: list[tuple[datetime, float]]  # the sales history of that item


class listItemsInfo(BaseModel):
    success: bool
    currency: str
    data: dict[str, ItemStats]

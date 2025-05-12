from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class NewestSale(BaseModel):
    item_name: Optional[str] = Field(None, alias="itemName")
    price: Optional[float] = None
    wear: Optional[float] = None
    date_sold: Optional[date] = Field(None, alias="dateSold")


class NewestSales(BaseModel):
    newest_sales_30days: list[NewestSale] = Field(alias="newestSales30Days")

from datetime import date
from pydantic import BaseModel, Field


class NewestSale(BaseModel):
    item_name: str | None = Field(None, alias="itemName")
    price: float | None = None
    wear: float | None = None
    date_sold: date | None = Field(None, alias="dateSold")


class NewestSales(BaseModel):
    newest_sales_30days: list[NewestSale] = Field(alias="newestSales30Days")

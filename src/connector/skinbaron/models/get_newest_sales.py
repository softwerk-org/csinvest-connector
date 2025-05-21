from datetime import date
from pydantic import BaseModel, Field


class NewestSale(BaseModel):
    item_name: str = Field(alias="itemName")
    price: float
    wear: float
    date_sold: date = Field(alias="dateSold")


class NewestSales(BaseModel):
    newest_sales_30days: list[NewestSale] = Field(alias="newestSales30Days")

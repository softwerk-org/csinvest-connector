from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from enum import Enum


class TxOperationType(Enum):
    Offer = "Offer"
    Order = "Order"


class LastSalesSale(BaseModel):
    price: float
    date: datetime
    tx_operation_type: TxOperationType = Field(alias="txOperationType")
    offer_attributes: dict[str, Any] = Field(alias="offerAttributes")
    order_attributes: dict[str, Any] = Field(alias="orderAttributes")


class LastSales(BaseModel):
    sales: list[LastSalesSale]

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from enum import Enum


class TxOperationType(Enum):
    Offer = "Offer"  # triggered by a seller’s offer
    Order = "Order"  # triggered by a buyer’s order
    Target = "Target"  # triggered by a buyer’s target (automated purchase request)


class LastSalesSale(BaseModel):
    price: float
    date: datetime
    tx_operation_type: TxOperationType = Field(alias="txOperationType")
    offer_attributes: dict[str, Any] = Field(alias="offerAttributes")
    order_attributes: dict[str, Any] = Field(alias="orderAttributes")


class LastSales(BaseModel):
    sales: list[LastSalesSale]

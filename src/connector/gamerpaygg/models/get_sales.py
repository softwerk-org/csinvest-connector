from datetime import datetime
from pydantic import BaseModel, Field, RootModel


class Sale(BaseModel):
    floatvalue: float
    price: float
    sold_at: datetime = Field(alias="soldAt")


class Sales(RootModel[dict[str, list[Sale]]]):
    root: dict[str, list[Sale]]

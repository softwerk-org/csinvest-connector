from pydantic import BaseModel, Field, RootModel


class Sale(BaseModel):
    floatvalue: float
    price: float
    sold_at: int = Field(alias="soldAt")


class Sales(RootModel[dict[str, list[Sale]]]):
    root: dict[str, list[Sale]]

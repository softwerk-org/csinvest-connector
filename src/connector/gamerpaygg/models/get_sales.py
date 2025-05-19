from pydantic import BaseModel, RootModel


class Sale(BaseModel):
    floatvalue: float | None = None
    price: float | None = None
    soldAt: int | None = None


class Sales(RootModel[dict[str, list[Sale]]]):
    root: dict[str, list[Sale]]

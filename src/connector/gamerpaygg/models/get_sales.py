from typing import Optional
from pydantic import BaseModel, RootModel


class Sale(BaseModel):
    floatvalue: Optional[float] = None
    price: Optional[int] = None
    soldAt: Optional[int] = None


class Sales(RootModel[dict[str, list[Sale]]]):
    pass

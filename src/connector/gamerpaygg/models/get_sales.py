from typing import Optional, List
from pydantic import BaseModel, RootModel


class Sale(BaseModel):
    floatvalue: Optional[float] = None
    price: Optional[int] = None
    soldAt: Optional[int] = None


class Sales(RootModel[List[Sale]]):
    """List of sales from GamerPayGG"""

    root: List[Sale]

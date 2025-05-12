from typing import Optional, List, Dict
from pydantic import BaseModel, RootModel


class Sale(BaseModel):
    floatvalue: Optional[float] = None
    price: Optional[float] = None
    soldAt: Optional[int] = None


class Sales(RootModel[Dict[str, List[Sale]]]):
    root: Dict[str, List[Sale]]

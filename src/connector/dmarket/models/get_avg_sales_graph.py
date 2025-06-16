from datetime import date
from pydantic import BaseModel


class AvgSalesGraph(BaseModel):
    totalSales: list[int]
    date: list[date]
    avgPrice: list[float]

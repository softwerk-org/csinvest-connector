from pydantic import BaseModel


class AvgSalesGraph(BaseModel):
    totalSales: list[str]
    date: list[str]
    avgPrice: list[str]

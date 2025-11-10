from pydantic import BaseModel, TypeAdapter


class PriceListEntry(BaseModel):
    market_hash_name: str
    qty: int
    min_price: int


PriceListResponse = TypeAdapter(list[PriceListEntry])

from typing import List
from pydantic import BaseModel, TypeAdapter


class Price(BaseModel):
    market_hash_name: str
    price: float  # Price value in USD
    market_product_link: str
    market_product_count: int
    cheapest_asset_id: int
    cheapest_float: str | None = None
    paint_index: int
    paint_seed: int
    inspect_link: str


Prices = TypeAdapter(list[Price])

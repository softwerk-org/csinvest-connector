from typing import Annotated

from pydantic import BaseModel


class PriceHistory(BaseModel):
    success: bool
    price_prefix: str
    price_suffix: str
    prices: Annotated[
        list[tuple[str, float, int]],
        """List of prices with date, price and volume.
        e.g. [('May 07 2025 06: +0', 5, 47)]""",
    ]

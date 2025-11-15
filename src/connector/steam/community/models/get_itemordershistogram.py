from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class ItemOrdersHistogram(BaseModel):
    success: bool
    sell_order_table: Optional[str] = None
    sell_order_summary: Optional[str] = None
    buy_order_table: Optional[str] = None
    buy_order_summary: Optional[str] = None
    highest_buy_order: Optional[int] = None
    lowest_sell_order: Optional[int] = None
    buy_order_graph: Optional[List[List[Union[float, str]]]] = None
    sell_order_graph: Optional[List[List[Union[float, str]]]] = None
    graph_max_y: Optional[int] = None
    graph_min_x: Optional[float] = None
    graph_max_x: Optional[float] = None
    price_prefix: Optional[str] = None
    price_suffix: Optional[str] = None

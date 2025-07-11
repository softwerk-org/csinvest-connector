from __future__ import annotations
from typing import Any

from connector.base import Connector
from connector.csfloat.models.get_listings import Listing, Listings
from connector.csfloat.models.get_similar_listings import SimilarListings
from connector.csfloat.models.get_history_graph import HistoryGraph, HistoryGraphEntry
from connector.csfloat.models.get_iteminfo import ItemInfoResponse


class CSFloatConnector(Connector):
    """Connector for the CSFloat REST API.

    Documentation: https://docs.csfloat.com/#introduction
    """

    def __init__(self, api_key: str, proxy_url: str | None = None):
        super().__init__(
            base_url="https://csfloat.com",
            proxy_url=proxy_url,
        )
        self.api_key = api_key

    async def get_listings(
        self,
        page: int = 0,
        limit: int = 50,
        sort_by: str = "best_deal",
        category: int = 0,
        def_index: list[int] | None = None,
        min_float: float | None = None,
        max_float: float | None = None,
        rarity: int | None = None,
        paint_seed: int | None = None,
        paint_index: int | None = None,
        user_id: str | None = None,
        collection: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        market_hash_name: str | None = None,
        type: str | None = None,
        stickers: str | None = None,
    ) -> Listings:
        """Get all active listings with optional filters."""
        assert limit <= 50, "Limit must be less than or equal to 50"
        params: dict[str, Any] = {
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "category": category,
        }
        if def_index is not None:
            params["def_index"] = def_index
        if min_float is not None:
            params["min_float"] = min_float
        if max_float is not None:
            params["max_float"] = max_float
        if rarity is not None:
            params["rarity"] = rarity
        if paint_seed is not None:
            params["paint_seed"] = paint_seed
        if paint_index is not None:
            params["paint_index"] = paint_index
        if user_id is not None:
            params["user_id"] = user_id
        if collection is not None:
            params["collection"] = collection
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if market_hash_name is not None:
            params["market_hash_name"] = market_hash_name
        if type is not None:
            params["type"] = type
        if stickers is not None:
            params["stickers"] = stickers

        text = await self._get(
            "/api/v1/listings",
            params=params,
            headers={
                "Authorization": f"{self.api_key}",
            },
        )
        listings = Listings.model_validate_json(text)
        return listings

    async def get_similar_listings(
        self,
        listing_id: str,
    ) -> list[Listing]:
        """Get listings similar to a given listing ID."""
        text = await self._get(
            f"/api/v1/listings/{listing_id}/similar",
            headers={
                "Authorization": f"{self.api_key}",
            },
        )
        return SimilarListings.validate_json(text)

    async def get_history_graph(
        self,
        market_hash_name: str,
    ) -> list[HistoryGraphEntry]:
        """Get sales price history graph data for a given market hash name."""
        text = await self._get(
            f"/api/v1/history/{market_hash_name}/graph",
            headers={
                "Authorization": f"{self.api_key}",
            },
        )
        return HistoryGraph.validate_json(text)

    async def get_iteminfo(self, inspect_link: str) -> ItemInfoResponse:
        """Get iteminfo for an item via its Steam inspect link."""
        text = await self._get(
            "https://api.csgofloat.com/",
            params={"url": inspect_link},
            headers={
                "Authorization": f"{self.api_key}",
                "Origin": "https://csfloat.com",
            },
        )
        return ItemInfoResponse.model_validate_json(text)

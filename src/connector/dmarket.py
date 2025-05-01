from datetime import datetime
from typing import Literal
from urllib.parse import urlencode

from nacl.bindings import crypto_sign

from .base import BaseConnector


class DMarketConnector(BaseConnector):
    base = "https://api.dmarket.com"
    __docs__ = "https://docs.dmarket.com/v1/swagger.html"

    def __init__(
        self,
        proxy_url: str | None = None,
        public_key: str | None = None,
        private_key: str | None = None,
    ):
        super().__init__(proxy_url=proxy_url)
        self.public_key = public_key
        self.private_key = private_key

    async def _auth_headers(
        self,
        method: str,
        path: str,
        params: dict | None = None,
    ) -> dict:
        assert self.public_key and self.private_key, (
            "Public and private key is required for authenticated requests"
        )
        nonce = str(round(datetime.now().timestamp()))
        return {
            "X-Api-Key": self.public_key,
            "X-Sign-Date": nonce,
            "X-Request-Sign": "dmar ed25519 "
            + crypto_sign(
                (method + path + "?" + urlencode(params or {}) + nonce).encode("utf-8"),
                bytes.fromhex(self.private_key),
            )[:64].hex(),
        }

    async def get_last_sales(
        self,
        market_hash_name: str,
        tx_operation_type: Literal["Target", "Offer"],
        limit: int = 500,
        offset: int = 0,
        filters: list[str] | None = None,
        game_id: str = "a8db",
    ):
        """Get the item sales history. Up to 12 last months."""
        method = "GET"
        path = "/trade-aggregator/v1/last-sales"
        params = {
            "title": market_hash_name,
            "gameId": game_id,
            "limit": limit,
            "offset": offset,
        }
        if filters:
            params["filters"] = filters
        if tx_operation_type:
            params["txOperationType"] = tx_operation_type

        response = await self._request(
            method,
            path,
            params=params,
            headers=await self._auth_headers(method, path, params),
            handler=lambda r: r.json(),
        )
        return response

    async def get_market_items(
        self,
        market_hash_name: str,
        game_id: str = "a8db",
        currency: str = "USD",
        order_by: str = "best_deals",
        order_dir: str = "desc",
        price_from: int = 0,
        price_to: int = 0,
        tree_filters: str | None = "",
        types: str = "dmarket",
        cursor: str | None = "",
        limit: int = 100,
        platform: str = "browser",
        is_logged_in: bool = True,
    ):
        """Get the list of unique items with `market_hash_name` that are available for purchase on DMarket."""

        response = await self._request(
            "GET",
            "/exchange/v1/market/items",
            params={
                "gameId": game_id,
                "title": market_hash_name,
                "currency": currency,
                "orderBy": order_by,
                "orderDir": order_dir,
                "priceFrom": price_from,
                "priceTo": price_to,
                "treeFilters": tree_filters,
                "types": types,
                "cursor": cursor,
                "limit": limit,
                "platform": platform,
                "isLoggedIn": is_logged_in,
            },
            proxied=True,
            handler=lambda r: r.json(),
        )
        return response

    async def get_aggregated_prices(
        self,
        market_hash_names: list[str] | str | None = None,
        limit: int | None = None,  # 10000 is the maximum limit
        offset: int | None = None,
    ):
        """Get the best market prices grouped by `market_hash_name`."""
        params = {}

        if market_hash_names:
            params["Titles"] = market_hash_names

        if limit:
            params["Limit"] = limit

        if offset:
            params["Offset"] = offset

        response = await self._request(
            "GET",
            "/price-aggregator/v1/aggregated-prices",
            params=params,
            proxied=True,
            handler=lambda r: r.json(),
        )
        return response

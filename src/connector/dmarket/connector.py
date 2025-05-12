from typing import Literal
from connector.base import Connector
from connector.dmarket.auth import DMarketAuth
from .models.get_last_sales import LastSales
from .models.get_market_items import MarketItems
from .models.get_aggregated_prices import AggregatedPrices


class DMarketConnector:
    __docs__ = "https://docs.dmarket.com/v1/swagger.html"

    def __init__(
        self,
        proxy: str | None = None,
        public_key: str | None = None,
        private_key: str | None = None,
    ):
        self.connector = Connector(
            base_url="https://api.dmarket.com",
            proxy=proxy,
        )
        self.auth = DMarketAuth(public_key=public_key, private_key=private_key)

    async def get_last_sales(
        self,
        market_hash_name: str,
        tx_operation_type: Literal["Target", "Offer"],
        limit: int = 500,
        offset: int = 0,
        filters: list[str] | None = None,
        game_id: str = "a8db",
    ) -> LastSales:
        """Get the item sales history. Up to 12 last months."""
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

        text = await self.connector.get(
            path,
            params=params,
            headers=await self.auth.headers("GET", path, params),
        )
        return LastSales.model_validate_json(text)

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
    ) -> MarketItems:
        """Get the list of unique items with `market_hash_name` that are available for purchase on DMarket."""

        text = await self.connector.get(
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
        )
        return MarketItems.model_validate_json(text)

    async def get_aggregated_prices(
        self,
        market_hash_names: list[str],
        limit: int = 100,
        offset: int = 0,
    ) -> AggregatedPrices:
        """Get the best market prices grouped by `market_hash_name`."""
        assert limit <= 10000, "Limit must be <= 10000"

        text = await self.connector.get(
            "/price-aggregator/v1/aggregated-prices",
            params={"Limit": limit, "Offset": offset, "Titles": market_hash_names},
        )
        return AggregatedPrices.model_validate_json(text)

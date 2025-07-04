from typing import Literal
from connector.base import Connector
from connector.dmarket.auth import DMarketAuth
from connector.errors import AuthParamsError

from .models.get_aggregated_prices import AggregatedPrices
from .models.get_avg_sales_graph import AvgSalesGraph
from .models.get_last_sales import LastSales, TxOperationType
from .models.get_market_items import MarketItems


class DMarketConnector(Connector):
    """
    https://docs.dmarket.com/v1/swagger.html
    """

    def __init__(
        self,
        proxy_url: str | None = None,
        public_key: str | None = None,
        private_key: str | None = None,
    ):
        super().__init__(
            base_url="https://api.dmarket.com",
            proxy_url=proxy_url,
        )
        self.public_key = public_key
        self.private_key = private_key

    async def get_last_sales(
        self,
        market_hash_name: str,
        limit: int = 500,
        offset: int = 0,
        tx_operation_type: TxOperationType | None = None,
        filters: list[str] | None = None,
        game_id: str = "a8db",
    ) -> LastSales:
        """Get the item sales history. Up to 12 last months."""
        assert self.public_key and self.private_key, (
            "public_key and private_key must be provided"
        )
        path = "/trade-aggregator/v1/last-sales"
        params = {
            "gameId": game_id,
            "limit": limit,
            "offset": offset,
        }
        if market_hash_name:
            params["title"] = market_hash_name
        if filters:
            params["filters"] = filters
        if tx_operation_type:
            params["txOperationType"] = tx_operation_type

        headers = DMarketAuth.get_headers(
            public_key=self.public_key,
            private_key=self.private_key,
            method="GET",
            path=path,
            params=params,
        )
        text = await self._get(
            path,
            params=params,
            headers=headers,
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

        text = await self._get(
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
        limit: int | None = None,
        offset: int | None = None,
    ) -> AggregatedPrices:
        """Get the best market prices grouped by `market_hash_name`."""
        assert limit is None or limit <= 10000, "Limit must be <= 10000"

        text = await self._get(
            "/price-aggregator/v1/aggregated-prices",
            params={
                "Limit": limit or len(market_hash_names),
                "Offset": offset or 0,
                "Titles": market_hash_names,
            },
        )
        return AggregatedPrices.model_validate_json(text)

    async def get_avg_sales_graph(
        self,
        title: str,
        game_id: str = "a8db",
        period: Literal["7D", "1M", "6M", "1Y"] = "1Y",
    ) -> AvgSalesGraph:
        """Get average sales graph data for a given title."""
        text = await self._get(
            "/trade-aggregator/v1/avg-sales-graph",
            params={
                "title": title,
                "gameId": game_id,
                "period": period,
            },
        )
        return AvgSalesGraph.model_validate_json(text)

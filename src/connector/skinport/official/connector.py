from connector.base import Connector
from .models.get_items import Items, Item
from .models.get_sales_history import SalesHistory, SalesItem


class SkinportOfficialConnector(Connector):
    """Connector for the Skinport Official REST API.

    Documentation: https://docs.skinport.com/
    """

    def __init__(self, proxy_url: str | None = None):
        super().__init__(base_url="https://api.skinport.com", proxy_url=proxy_url)

    async def get_items(
        self,
        appid: int = 730,
        currency: str = "USD",
        tradable: int = 0,
    ) -> list[Item]:
        """Provides a list of listings on the marketplace."""
        params = {
            "app_id": appid,
            "currency": currency,
            "tradable": tradable,
        }
        text = await self._get(
            "/v1/items",
            headers={"Accept-Encoding": "br"},
            params=params,
            timeout=30,
        )
        items = Items.model_validate_json(text)
        return items.root

    async def get_sales_history_agg(
        self,
        market_hash_names: list[str] | None = None,
        appid: int = 730,
        currency: str = "USD",
    ) -> list[SalesItem]:
        """
        Provides an aggregated Sales History.
        Will return a list of all items when no market_hash_names are provided.
        """
        params: dict[str, str | int] = {
            "app_id": appid,
            "currency": currency,
        }
        if market_hash_names is not None:
            params["market_hash_name"] = ",".join(market_hash_names)
        text = await self._get(
            "/v1/sales/history",
            headers={"Accept-Encoding": "br"},
            params=params,
            timeout=30,
        )
        stats = SalesHistory.model_validate_json(text)
        return stats.root

from connector.base import Connector
from .models.get_items import Items, ItemsItem
from .models.get_sales_history import SalesHistory, SalesItem


class SkinportConnector(Connector):
    """Connector for the Skinport API.

    Documentation: https://docs.skinport.com/
    """

    def __init__(self, proxy: str | None = None):
        super().__init__(base_url="https://api.skinport.com", proxy=proxy)

    async def get_items(
        self,
        appid: int = 730,
        currency: str = "USD",
        tradable: int = 0,
    ) -> list[ItemsItem]:
        params = {"app_id": appid, "currency": currency, "tradable": tradable}
        text = await self._get(
            "/v1/items",
            headers={"Accept-Encoding": "br"},
            params=params,
            timeout=30,
        )
        items = Items.model_validate_json(text)
        return items.root

    async def get_sales_history(
        self,
        market_hash_names: list[str] | None = None,
        appid: int = 730,
        currency: str = "USD",
    ) -> list[SalesItem]:
        """
        Provides aggregated Sales.
        Will return list of sales history for each market_hash_name if no market_hash_names are provided
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

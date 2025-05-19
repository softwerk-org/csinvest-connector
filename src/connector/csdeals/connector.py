from typing import Any, final
from pydantic import BaseModel, TypeAdapter, conlist
from connector.base import Connector
from connector.csdeals.auth import CsDealsAuth
from connector.csdeals.models.get_lowest_prices import LowestPrices
from connector.csdeals.models.get_sales_history import SalesHistory
from connector.csdeals.models.get_sales_history_multi import SalesHistoryMulti


@final
class CSDealsConnector(Connector):
    """https://cs.deals/es/API-documentation"""

    def __init__(
        self,
        api_key: str | None = None,
        proxy: str | None = None,
    ):
        super().__init__(
            base_url="https://cs.deals/API",
            proxy=proxy,
        )
        if api_key is not None:
            self.auth = CsDealsAuth(api_key=api_key)

    async def get_lowest_prices(self, app_id: int = 730) -> LowestPrices:
        """Get the lowest prices for all items."""
        text = await self._post(
            "/IPricing/GetLowestPrices/v1",
            json={"appid": app_id},
        )
        return LowestPrices.model_validate_json(text)

    async def get_sales_history(
        self, name: str, appid: int = 730, phase: str | None = None
    ) -> SalesHistory:
        """Get the sales history for a given item."""
        text = await self._post(
            "/IPricing/GetSalesHistory/v1",
            json={
                "name": name,
                "appid": appid,
                **({"phase": phase} if phase else {}),
            },
        )
        return SalesHistory.model_validate_json(text)

    class Item(BaseModel):
        name: str
        appid: int
        phase: str | None = None

    items = TypeAdapter(conlist(Item, max_length=50))

    async def get_sales_history_multi(
        self, items: list[Item] | list[dict[str, Any]]
    ) -> SalesHistoryMulti:
        """Get the sales history for a list of items."""
        validated = self.items.validate_python(items)

        text = await self._post(
            "/IPricing/GetSalesHistoryMulti/v1",
            json={"items": [item.model_dump(exclude_none=True) for item in validated]},
        )
        return SalesHistoryMulti.model_validate_json(text)

from connector.base import Connector
from .models.get_latest_rates import LatestRates


class OpenExchangeRatesConnector:
    __docs__ = "https://open.er-api.com/documentation"

    def __init__(self, proxy: str | None = None):
        self.connector = Connector(
            base_url="https://open.er-api.com",
            proxy=proxy,
        )

    async def get_latest_rates(self, base_code: str = "USD") -> LatestRates:
        text = await self.connector.get(
            f"/v6/latest/{base_code}",
        )
        return LatestRates.model_validate_json(text)

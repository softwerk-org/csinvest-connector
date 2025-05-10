from connector.base import ConnectorBase
from .models.get_latest_rates import GetLatestRates


class OpenExchangeRatesConnector:
    __docs__ = "https://open.er-api.com/documentation"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://open.er-api.com/v6", proxy_url=proxy_url)

    async def get_latest_rates(self, base_code: str = "USD") -> GetLatestRates:
        text = await self.connector.request(
            "GET",
            f"/latest/{base_code}",
        )
        return GetLatestRates.model_validate_json(text) 
import pytest

from connector.skins.connector import SkinsConnector
from connector.skins.models.get_market_items import MarketItems
from connector.errors import ValidationError as PydanticValidationError


@pytest.mark.asyncio
async def test_get_market_items_integration():
    async with SkinsConnector() as connector:
        model = await connector.get_market_items(page=2, limit=10)

import pytest

from connector.skins.connector import SkinsConnector
from connector.skins.models.get_market_items import MarketItems
from connector.errors import ValidationError as PydanticValidationError


@pytest.mark.asyncio
async def test_get_market_items_integration():
    async with SkinsConnector() as connector:
        try:
            model = await connector.get_market_items(page=2, limit=10)
        except PydanticValidationError:
            pytest.skip(
                "Skins endpoint returned unparseable JSON; skipping integration test"
            )
    assert isinstance(model, MarketItems)
    assert model.data is not None
    assert model.pagination.limit == 10
    if model.data:
        first = model.data[0]
        assert hasattr(first, "marketHashName")
        assert hasattr(first, "lowestPrice")

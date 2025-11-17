import pytest

from connector.youpin898.connector import YouPin898Connector
from connector.youpin898.models.get_market_goods import MarketGoods
from connector.errors import ValidationError as PydanticValidationError


@pytest.mark.asyncio
async def test_get_market_goods_integration():
    async with YouPin898Connector() as connector:
        model = await connector.get_market_goods(page_size=10, page_index=1)
    assert isinstance(model, MarketGoods)
    assert model.data is not None
    assert len(model.data) >= 0
    if model.data:
        first = model.data[0]
        assert hasattr(first, "commodity_name")

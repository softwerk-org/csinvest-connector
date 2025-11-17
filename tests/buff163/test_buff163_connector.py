import pytest

from connector.buff163.connector import Buff163Connector
from connector.buff163.models.get_market_goods import MarketGoods
from connector.errors import ValidationError as PydanticValidationError


@pytest.mark.asyncio
async def test_get_market_goods_integration():
    async with Buff163Connector() as connector:
        model = await connector.get_market_goods(page_num=1, page_size=10)
    assert isinstance(model, MarketGoods)
    assert model.data is not None
    assert hasattr(model.data, "items")
    if model.data.items:
        first = model.data.items[0]
        assert hasattr(first, "market_hash_name") or hasattr(first, "name")

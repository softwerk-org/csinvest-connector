import os
import time
import pytest

from connector.buffmarket.connector import BuffMarketConnector
from connector.buffmarket.models.get_market_goods import MarketGoods
from connector.errors import ValidationError as PydanticValidationError


@pytest.mark.asyncio
async def test_get_market_goods_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with BuffMarketConnector(
        steam_username=username,
        steam_password=password,
        steam_api_key=api_key,
    ) as connector:
        model = await connector.get_market_goods(page_num=2, page_size=100)

import pytest
import os

from connector.skinbaron.connector import SkinbaronConnector


@pytest.mark.asyncio
async def test_get_price_list_integration():
    api_key = os.getenv("SKINBARON_API_KEY")
    if not api_key:
        pytest.skip("SKINBARON_API_KEY required for integration tests")
    async with SkinbaronConnector(api_key=api_key) as connector:
        model = await connector.get_price_list()
    assert model.map is not None


@pytest.mark.asyncio
async def test_get_best_deals_integration():
    api_key = os.getenv("SKINBARON_API_KEY")
    if not api_key:
        pytest.skip("SKINBARON_API_KEY required for integration tests")
    async with SkinbaronConnector(api_key=api_key) as connector:
        model = await connector.get_best_deals()
    assert model.best_deals is not None


@pytest.mark.asyncio
async def test_get_newest_sales_integration():
    api_key = os.getenv("SKINBARON_API_KEY")
    if not api_key:
        pytest.skip("SKINBARON_API_KEY required for integration tests")
    async with SkinbaronConnector(api_key=api_key) as connector:
        model = await connector.get_newest_sales("AK-47 | Redline (Minimal Wear)")
    assert model.newest_sales_30days is not None

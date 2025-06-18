import os
import pytest

from connector.skinport.connector import SkinportConnector
from connector.skinport.models.get_item import ItemResponse


@pytest.mark.asyncio
async def test_skinport_get_items_integration():
    async with SkinportConnector() as connector:
        items = await connector.get_items()
    assert isinstance(items, list)
    assert items, "Expected non-empty list of items"
    first = items[0]
    assert hasattr(first, "market_hash_name")
    assert hasattr(first, "min_price")


@pytest.mark.asyncio
async def test_skinport_get_sales_history_one():
    async with SkinportConnector() as connector:
        history = await connector.get_sales_history(["Snakebite Case"])
    assert history[0] is not None


@pytest.mark.asyncio
async def test_skinport_get_sales_history_multiple():
    async with SkinportConnector() as connector:
        history = await connector.get_sales_history(
            ["Snakebite Case", "Revolution Case"]
        )
    assert isinstance(history, list)
    assert history[0] is not None


@pytest.mark.asyncio
async def test_skinport_get_sales_history_all():
    async with SkinportConnector() as connector:
        history = await connector.get_sales_history()
    assert isinstance(history, list)
    assert history[0] is not None


@pytest.mark.asyncio
async def test_skinport_get_item_integration():
    """Integration test for the public Skinport get_item endpoint."""
    async with SkinportConnector() as connector:
        response = await connector.get_item(
            "★ StatTrak™ Butterfly Knife | Tiger Tooth (Factory New)"
        )
    assert isinstance(response, ItemResponse)
    assert response.success is True
    assert len(response.data.history) > 0

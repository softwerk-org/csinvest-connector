import os
import pytest

from connector.skinport.unofficial.connector import SkinportUnofficialConnector
from connector.skinport.unofficial.models.get_item import ItemResponse


@pytest.mark.asyncio
async def test_skinport_public_get_item_integration():
    """Integration test for the public Skinport get_item endpoint."""
    flaresolverr = os.getenv("FLARESOLVERR_URL")
    if not flaresolverr:
        pytest.skip("FLARESOLVERR_URL required for integration tests")

    async with SkinportUnofficialConnector(flaresolverr_url=flaresolverr) as connector:
        response = await connector.get_item(
            "★ StatTrak™ Butterfly Knife | Tiger Tooth (Factory New)"
        )
    assert isinstance(response, ItemResponse)
    assert response.success is True
    assert len(response.data.history) > 0

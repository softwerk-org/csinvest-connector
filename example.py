from connector.steam import SteamConnector
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    steam = SteamConnector(
        # INSERT YOUR OWN CREDENTIALS
        username="XX",
        password="XX",
        api_key="XX",
    )
    try:
        price_history = await steam.community.get_pricehistory(
            market_hash_name="Chroma 2 Case",
            country="DE",
            currency=0,
            appid=730,
        )
        print(price_history)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    asyncio.run(main())

import logging
import os
import httpx
import tenacity


HTTPX_LOG_LEVEL = os.getenv("HTTPX_LOG_LEVEL", "ERROR")
logging.getLogger("httpx").setLevel(HTTPX_LOG_LEVEL)


DEFAULT_RETRY_KWARGS = {
    "stop": tenacity.stop_after_attempt(3),
    "wait": tenacity.wait_fixed(1),
    "retry": tenacity.retry_if_result(
        lambda r: isinstance(r, httpx.Response) and r.is_error()
    ),
}


class Connector:
    def __init__(
        self,
        base_url: str,
        proxy: str | None = None,
        logger: logging.Logger | None = None,
    ):
        self.client = httpx.AsyncClient(base_url=base_url, proxy=proxy)
        self.logger = logger or logging.getLogger(__name__)

    async def request(
        self,
        method: str,
        url: str,
        *,
        content: bytes | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        cookies: dict | None = None,
        headers: dict | None = None,
        timeout: int = 10,
        retrier: tenacity.AsyncRetrying | None = None,
    ) -> str:
        if retrier is None:
            retrier = tenacity.AsyncRetrying(**DEFAULT_RETRY_KWARGS)

        async for attempt in retrier:
            with attempt:
                async with self.client as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        content=content,
                        data=data,
                        params=params,
                        headers=headers,
                        follow_redirects=True,
                        json=json,
                        timeout=timeout,
                        cookies=cookies,
                    )
                    return response.text

    async def get(
        self,
        url: str,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        timeout: int = 10,
        retrier: tenacity.AsyncRetrying | None = None,
    ) -> str:
        return await self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            retrier=retrier,
        )

    async def post(
        self,
        url: str,
        *,
        content: bytes | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        timeout: int = 10,
        retrier: tenacity.AsyncRetrying | None = None,
    ) -> str:
        return await self.request(
            "POST",
            url,
            content=content,
            data=data,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            retrier=retrier,
        )

    async def close(self):
        await self.client.aclose()

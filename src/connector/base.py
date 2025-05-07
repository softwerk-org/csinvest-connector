import logging
from collections.abc import Callable
from typing import TypeVar

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

T = TypeVar("T")


class BaseConnector:
    base: str = ""

    def __init__(self, proxy_url: str | None = None, timeout: int = 10):
        self.proxy_url = proxy_url
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(BaseException),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        retry_error_callback=lambda _: None,
    )
    async def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        *,
        cookies: dict | None = None,
        headers: dict | None = None,
        body: dict | None = None,
        proxied: bool = False,
        handler: Callable[[httpx.Response], T] = lambda r: r,
    ) -> T:
        async with httpx.AsyncClient(
            headers=headers,
            proxy=self.proxy_url if proxied else None,
            timeout=self.timeout,
            cookies=cookies,
        ) as client:
            response = await client.request(
                method=method,
                url=self.base + path,
                params=params,
                headers=headers,
                json=body,
                follow_redirects=True,
            )
            response.raise_for_status()
            return handler(response)

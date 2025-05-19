import logging
import os
import httpx
from typing import Any, Self


HTTPX_LOG_LEVEL = os.getenv("HTTPX_LOG_LEVEL", "ERROR")
logging.getLogger("httpx").setLevel(HTTPX_LOG_LEVEL)


class Connector:
    def __init__(
        self,
        base_url: str,
        proxy: str | None = None,
        logger: logging.Logger | None = None,
    ):
        self.client = httpx.AsyncClient(base_url=base_url, proxy=proxy)
        self.logger = logger or logging.getLogger(__name__)

    async def _request(
        self,
        method: str,
        url: str,
        *,
        content: bytes | None = None,
        data: dict[str, Any] | None = None,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> str:
        response = await self.client.request(
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
        response.raise_for_status()
        return response.text

    async def _get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> str:
        return await self._request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        )

    async def _post(
        self,
        url: str,
        *,
        content: bytes | None = None,
        data: dict[str, Any] | None = None,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> str:
        return await self._request(
            "POST",
            url,
            content=content,
            data=data,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: Any,
    ) -> None:
        await self.client.aclose()

    async def close(self) -> None:
        await self.client.aclose()

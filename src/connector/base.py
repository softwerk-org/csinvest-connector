import logging

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



class ConnectorBase:
    def __init__(self, base_url: str, proxy_url: str | None = None, timeout: int = 10):
        self.base = base_url
        self.proxy_url = proxy_url
        self.timeout = timeout

    def retry_if_http_error(e: Exception) -> bool:
        return isinstance(e, httpx.HTTPStatusError) and e.response.status_code in [
            408,  # If Request timed out
            429,  # If Too Many Requests
            500,  # If Internal Server Error
            503,  # If Service Unavailable
            504,  # If Gateway Timeout
            520,  # If Unknown Error
            522,  # If Connection Timed Out
            524,  # If A Timeout Occurred
            599,  # If Network Connect Timeout Error
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(retry_if_http_error),
        before_sleep=before_sleep_log(logger, logging.INFO),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        *,
        cookies: dict | None = None,
        json: dict | None = None,
        headers: dict | None = None,
        use_proxy: bool = False,
    ) -> str:
        async with httpx.AsyncClient(
            headers=headers,
            proxy=self.proxy_url if use_proxy else None,
            timeout=self.timeout,
            cookies=cookies,
        ) as client:
            response = await client.request(
                method=method,
                url=self.base + path,
                params=params,
                headers=headers,
                follow_redirects=True,
                json=json,
            )
            response.raise_for_status()
            return response.text



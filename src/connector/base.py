from typing import Any, Self
from urllib.parse import urljoin
import hrequests
from hrequests.cookies import RequestsCookieJar


class Connector:
    def __init__(
        self,
        base_url: str = "",
        proxy_url: str | None = None,
    ):
        self.base_url = base_url
        self.session = hrequests.Session(
            proxy=proxy_url,
        )

    def _prepare_cookies(self, cookies: dict[str, Any] | None):
        """Convert a simple ``dict`` of cookies to a ``RequestsCookieJar``.

        hrequests 0.9.x has a bug that raises when a plain ``dict`` is supplied
        via the ``cookies`` parameter. Wrapping the values in a
        :class:`requests.cookies.RequestsCookieJar` side-steps the buggy code
        path. If ``cookies`` is already a non-dict (e.g. a CookieJar), it is
        returned unchanged.
        """
        if cookies is None or not isinstance(cookies, dict):
            return cookies

        jar = RequestsCookieJar()
        for name, value in cookies.items():
            jar.set(name, value)
        return jar

    async def _get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> str:
        return self.session.get(
            urljoin(self.base_url, url),
            params=params,
            headers=headers,
            cookies=self._prepare_cookies(cookies),
            timeout=timeout,
        ).text

    async def _post(
        self,
        url: str,
        *,
        data: dict[str, Any] | None = None,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> str:
        return self.session.post(
            urljoin(self.base_url, url),
            data=data,
            json=json,
            params=params,
            headers=headers,
            cookies=self._prepare_cookies(cookies),
            timeout=timeout,
        ).text

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: Any,
    ) -> None:
        self.session.close()

    async def close(self) -> None:
        self.session.close()

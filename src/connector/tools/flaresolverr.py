from types import TracebackType
import httpx
from typing import Any, Self
from urllib.parse import urlencode
from httpx import URL
from diskcache import Cache
import json
import hashlib

from pydantic import BaseModel


class Solution(BaseModel):
    url: str
    status: int
    headers: dict[str, str] | None = None
    response: str | None = None
    cookies: list[dict[str, Any]]
    userAgent: str


class Response(BaseModel):
    solution: Solution
    status: str
    message: str
    startTimestamp: int
    endTimestamp: int
    version: str


CMDS = {
    "GET": "request.get",
    "POST": "request.post",
    "SESSIONS_CREATE": "sessions.create",
    "SESSIONS_DESTROY": "sessions.destroy",
    "SESSIONS_LIST": "sessions.list",
}


class Flaresolverr:
    """Handles Cloudflare challenge solving via FlareSolverr"""

    def __init__(
        self,
        flaresolverr_url: str,
        session_id: str = "default",
        proxy_url: str | None = None,
        cache_response: bool = False,
        cache_ttl_min: int = 30,
    ):
        self.flaresolverr_url = flaresolverr_url
        self.session_id = session_id
        self.proxy_url = proxy_url
        self.cache = Cache(".flaresolverr")
        self.cache_ttl_min = cache_ttl_min
        self.cache_response = cache_response

    def __enter__(self) -> Self:
        self.sessions_create(self.session_id, self.proxy_url)
        return self

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        self.sessions_destroy(self.session_id)

    def sessions_create(self, id: str, proxy_url: str | None = None) -> str:
        payload: dict[str, Any] = {
            "cmd": CMDS["SESSIONS_CREATE"],
            "session": id,
        }
        if proxy_url:
            payload["proxy"] = {
                "url": proxy_url,
            }
        r = httpx.post(self.flaresolverr_url, json=payload)
        r.raise_for_status()
        return r.json()["session"]

    def sessions_destroy(self, id: str) -> None:
        payload = {
            "cmd": CMDS["SESSIONS_DESTROY"],
            "session": id,
        }
        r = httpx.post(self.flaresolverr_url, json=payload)
        r.raise_for_status()

    def sessions_list(self) -> list[str]:
        payload = {
            "cmd": CMDS["SESSIONS_LIST"],
        }
        r = httpx.post(self.flaresolverr_url, json=payload)
        r.raise_for_status()
        return r.json()["sessions"]

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        cookies: dict[str, str] | None = None,
        proxy_url: str | None = None,
        return_only_cookies: bool = False,
        timeout_s: int = 6,
        session: str | None = None,
        session_ttl_min: int = 30,
    ) -> Response:
        if method.upper() not in CMDS:
            raise ValueError(f"Method {method.upper()} not supported")

        payload: dict[str, Any] = {
            "cmd": CMDS[method.upper()],
            "url": url,
            "maxTimeout": timeout_s * 1000,
        }
        if proxy_url:
            payload["proxy"] = {
                "url": proxy_url,
            }

        if data:
            payload["postData"] = urlencode(data)

        if params:
            payload["url"] = str(URL(url, params=params))

        if cookies:
            payload["cookies"] = cookies

        if return_only_cookies:
            payload["returnOnlyCookies"] = True

        if session:
            payload["session"] = session
            payload["session_ttl_minutes"] = session_ttl_min

        key = ""
        if self.cache_response:
            key = hashlib.md5(
                json.dumps(payload, sort_keys=True).encode("utf-8")
            ).hexdigest()
            cached = self.cache.get(key)
            if cached:
                return Response.model_validate_json(cached)  # type: ignore

        r = httpx.post(
            self.flaresolverr_url,
            json=payload,
            timeout=timeout_s,
        )
        r.raise_for_status()
        model = Response.model_validate_json(r.text)
        if self.cache_response:
            self.cache.set(key, r.text, expire=self.cache_ttl_min * 60)
        return model

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        cookies: dict[str, str] | None = None,
        return_only_cookies: bool = False,
        proxy_url: str | None = None,
        session: str | None = None,
        session_ttl_min: int = 30,
        timeout_s: int = 6,
    ) -> Response:
        return self.request(
            "GET",
            url,
            params=params,
            cookies=cookies,
            proxy_url=proxy_url,
            return_only_cookies=return_only_cookies,
            timeout_s=timeout_s,
            session=session,
            session_ttl_min=session_ttl_min,
        )

    def post(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        cookies: dict[str, str] | None = None,
        return_only_cookies: bool = False,
        proxy_url: str | None = None,
        session: str | None = None,
        session_ttl_min: int = 30,
        timeout_s: int = 6,
    ) -> Response:
        return self.request(
            "POST",
            url,
            params=params,
            data=data,
            cookies=cookies,
            proxy_url=proxy_url,
            return_only_cookies=return_only_cookies,
            timeout_s=timeout_s,
            session=session,
            session_ttl_min=session_ttl_min,
        )

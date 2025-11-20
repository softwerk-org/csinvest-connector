from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import httpx

from diskcache import Cache
from typing import cast

from connector.steam.community.auth import SteamAuth


BUFF_CACHE = Cache(".buffauth")


class BuffMarketAuth:
    def __init__(
        self,
        steam_auth: SteamAuth,
        ttl: int = 30 * 60,
        cache: Cache = BUFF_CACHE,
    ) -> None:
        self.steam_auth = steam_auth
        self.ttl = ttl
        self.cache = cache
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }
        self.BUFF_LOGIN_URL = "https://api.buff.market/account/login/steam?remember=1"

    async def get_cookies(self) -> dict[str, str]:
        key = f"buff:{self.steam_auth.username}"
        if (cached := self.cache.get(key)) is not None:
            return cast(dict[str, str], cached)

        steam_cookies = await self.steam_auth.get_cookies()

        async with httpx.AsyncClient(
            headers=self.headers,
            follow_redirects=True,
        ) as session:
            session.cookies.update(steam_cookies)

            resp = await session.get(self.BUFF_LOGIN_URL)
            resp.raise_for_status()

            host = urlparse(str(resp.url)).hostname or ""

            if host.endswith("buff.market"):
                buff_cookies = self._extract_buff_cookies(session.cookies)
                self.cache.set(key, buff_cookies, expire=self.ttl)
                return buff_cookies

            if "steamcommunity.com" not in host:
                raise RuntimeError(f"Unexpected host after login start: {host}")

            soup = BeautifulSoup(resp.text, "html.parser")
            form = soup.find("form", {"id": "openidForm"})
            if form is None:
                raise RuntimeError(
                    "Could not find openidForm on Steam login page. "
                    "Check that steam_auth.get_cookies() returns a valid logged-in Steam session."
                )

            action_attr = form.get("action")
            if not action_attr:
                raise RuntimeError("openidForm has no action attribute")
            action_url = urljoin(str(resp.url), action_attr)

            post_payload: dict[str, str] = {}
            for input_tag in form.find_all("input"):
                name = input_tag.get("name")
                if not name:
                    continue
                value = input_tag.get("value", "")
                post_payload[name] = value

            files = {k: (None, v) for k, v in post_payload.items()}
            resp2 = await session.post(action_url, files=files, timeout=10)
            resp2.raise_for_status()

            host2 = urlparse(str(resp2.url)).hostname or ""
            if not host2.endswith("buff.market"):
                raise RuntimeError(
                    f"After OpenID POST we did not end up on buff.market, "
                    f"but on {host2}. Check Steam cookies and response HTML."
                )

            buff_cookies = self._extract_buff_cookies(session.cookies)
            self.cache.set(key, buff_cookies, expire=self.ttl)
            return buff_cookies

    def _extract_buff_cookies(self, cookie_jar: httpx.Cookies) -> dict[str, str]:
        buff_cookies: dict[str, str] = {}
        for c in cookie_jar.jar:
            if not c.domain or not c.domain.endswith("buff.market"):
                continue

            if c.name in (
                "csrf_token",
                "client_id",
                "Device-Id",
                "session",
                "remember_me",
            ):
                buff_cookies[c.name] = c.value

        return buff_cookies

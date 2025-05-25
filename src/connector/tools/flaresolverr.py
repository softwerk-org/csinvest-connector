from typing import cast
import httpx
from diskcache import Cache

cache = Cache(".flaresolverr")


class Flaresolverr:
    """Handles Cloudflare challenge solving via FlareSolverr, caching cookies until expiry."""

    def __init__(self):
        pass

    def solve(self, url, flaresolverr_url, proxy_url: str | None = None):
        key = (url, flaresolverr_url, proxy_url)
        cached = cache.get(key)
        if cached:
            return cast(tuple[dict[str, str], str], cached)  # returns (cookies, ua)

        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60_000,
        }
        if proxy_url:
            payload["proxy_url"] = proxy_url

        r = httpx.post(
            flaresolverr_url,
            json=payload,
            timeout=payload["maxTimeout"] / 1000,
        )
        r.raise_for_status()
        sol = r.json()["solution"]
        cookies_list = sol.get("cookies", [])
        cookies = {c["name"]: c["value"] for c in cookies_list}
        user_agent = sol.get("userAgent", "")

        # cache expires every 30 minutes
        cache.set(key, (cookies, user_agent), expire=30 * 60)
        return cookies, user_agent

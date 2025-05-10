import asyncio
import json
import os
import random
import time
from base64 import b64encode

import httpx
from rsa import PublicKey, encrypt


class SteamAuthError(Exception):
    """Raised on Steam authentication failures."""

    pass


class SteamAuth:
    """
    Asynchronous Steam WebAPI login cookie provider with caching.

    Steps:
      1) Fetch RSA key
      2) Perform credential login
      3) Poll for access_token
      4) Build cookies (steamLoginSecure & sessionid)
      5) Cache cookies in JSON file for `ttl` seconds
    """

    RSA_KEY_URL = (
        "https://api.steampowered.com/IAuthenticationService/GetPasswordRSAPublicKey/v1"
    )
    AUTH_URL = (
        "https://api.steampowered.com/"
        "IAuthenticationService/BeginAuthSessionViaCredentials/v1"
    )
    POLL_URL = (
        "https://api.steampowered.com/IAuthenticationService/PollAuthSessionStatus/v1"
    )

    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        cache_file: str = "steam_cookie_cache.json",
        ttl: int = 30 * 60,
    ) -> None:
        self.username = username
        self._password = password
        self.api_key = api_key
        self.cache_file = cache_file
        self.ttl = ttl

    async def _get_rsa_key(self, client: httpx.AsyncClient) -> tuple[PublicKey, int]:
        """Fetch RSA public key and timestamp from Steam WebAPI."""
        resp = await client.get(
            self.RSA_KEY_URL,
            params={"key": self.api_key, "account_name": self.username},
        )
        resp.raise_for_status()
        data = resp.json().get("response", {})
        try:
            mod = int(data["publickey_mod"], 16)
            exp = int(data["publickey_exp"], 16)
            ts = int(data["timestamp"])
        except KeyError as e:
            raise SteamAuthError(f"Missing RSA key field: {e}")
        return PublicKey(mod, exp), ts

    async def login(self, client: httpx.AsyncClient) -> tuple[str, str]:
        """Perform credential login and return (steamid, access_token)."""
        pubkey, ts = await self._get_rsa_key(client)
        encrypted = b64encode(encrypt(self._password.encode(), pubkey)).decode()

        resp = await client.post(
            self.AUTH_URL,
            params={"key": self.api_key},
            data={
                "account_name": self.username,
                "encrypted_password": encrypted,
                "encryption_timestamp": ts,
            },
        )
        resp.raise_for_status()
        info = resp.json().get("response", {})
        steamid = info.get("steamid")
        cid = info.get("client_id")
        rid = info.get("request_id")
        if not all((steamid, cid, rid)):
            raise SteamAuthError(
                "Login initiation missing steamid/client_id/request_id"
            )

        token = await self._poll_status(client, cid, rid)
        return steamid, token

    async def _poll_status(
        self, client: httpx.AsyncClient, client_id: str, request_id: str
    ) -> str:
        """Poll Steam WebAPI until an access_token is available."""
        while True:
            resp = await client.post(
                self.POLL_URL,
                params={"key": self.api_key},
                data={"client_id": client_id, "request_id": request_id},
            )
            resp.raise_for_status()
            data = resp.json().get("response", {})
            if not data.get("had_remote_interaction", True):
                token = data.get("access_token") or data.get("accessToken")
                if not token:
                    raise SteamAuthError("Poll returned no access_token")
                return token
            await asyncio.sleep(1)

    def _load_cache(self) -> dict[str, str] | None:
        """Load cached cookies if cache_file exists and is fresh."""
        if not os.path.exists(self.cache_file):
            return None
        try:
            with open(self.cache_file) as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return None
        if time.time() - data.get("timestamp", 0) < self.ttl:
            return data.get("cookies")
        return None

    def _save_cache(self, cookies: dict[str, str]) -> None:
        """Save cookies to cache_file with current timestamp."""
        with open(self.cache_file, "w") as f:
            json.dump({"timestamp": time.time(), "cookies": cookies}, f)

    async def cookies(self) -> dict[str, str]:
        """Return cached or freshly generated cookies."""
        if cached := self._load_cache():
            return cached

        async with httpx.AsyncClient() as client:
            steamid, token = await self.login(client)
            secure = f"{steamid}%7C%7C{token}"
            sessionid = "".join(str(random.randint(0, 9)) for _ in range(17))
            cookies = {"steamLoginSecure": secure, "sessionid": sessionid}

            self._save_cache(cookies)
            return cookies

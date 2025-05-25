from typing import cast
from diskcache import Cache
import asyncio
import random
from base64 import b64encode

import httpx
from rsa import PublicKey, encrypt


STEAM_CACHE = Cache(".steamauth")


class SteamAuthError(Exception):
    """Raised on Steam authentication failures."""


class SteamAuth:
    """
    Asynchronous Steam WebAPI login cookie provider with caching.
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
        ttl: int = 30 * 60,  # 30 minutes
        cache: Cache = STEAM_CACHE,
    ) -> None:
        self.username = username
        self._password = password
        self.api_key = api_key
        self.ttl = ttl
        self.cache = cache

    async def cookies(self) -> dict[str, str]:
        """Return cached cookies or perform a fresh login and cache them."""
        key = f"steam:{self.username}"
        if (cached := self.cache.get(key)) is not None:
            return cast(dict[str, str], cached)

        async with httpx.AsyncClient() as client:
            steamid, token = await self._login(client)
            secure = f"{steamid}%7C%7C{token}"
            sessionid = "".join(str(random.randint(0, 9)) for _ in range(17))
            cookies = {"steamLoginSecure": secure, "sessionid": sessionid}

            self.cache.set(key, cookies, expire=self.ttl)
            return cookies

    async def _get_rsa_key(self, client: httpx.AsyncClient) -> tuple[PublicKey, int]:
        resp = await client.get(
            self.RSA_KEY_URL,
            params={"key": self.api_key, "account_name": self.username},
        )
        resp.raise_for_status()
        data = resp.json()["response"]
        try:
            mod = int(data["publickey_mod"], 16)
            exp = int(data["publickey_exp"], 16)
            ts = int(data["timestamp"])
        except KeyError as e:
            raise SteamAuthError(f"Missing RSA key field: {e}")
        return PublicKey(mod, exp), ts

    async def _login(self, client: httpx.AsyncClient) -> tuple[str, str]:
        """Full login dance, returns (steamid, access_token)."""
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
        info = resp.json()["response"]
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
        while True:
            resp = await client.post(
                self.POLL_URL,
                params={"key": self.api_key},
                data={"client_id": client_id, "request_id": request_id},
            )
            resp.raise_for_status()
            data = resp.json()["response"]
            if not data.get("had_remote_interaction", True):
                token = data.get("access_token") or data.get("accessToken")
                if not token:
                    raise SteamAuthError("Poll returned no access_token")
                return token
            await asyncio.sleep(1)

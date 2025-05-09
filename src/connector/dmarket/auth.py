from datetime import datetime
from urllib.parse import urlencode

from nacl.bindings import crypto_sign

class DMarketAuth:
    def __init__(self, public_key: str, private_key: str):
        self.public_key = public_key
        self.private_key = private_key

    async def headers(
        self,
        method: str,
        path: str,
        params: dict | None = None,
    ) -> dict:
        assert self.public_key and self.private_key, (
            "Public and private key is required for authenticated requests"
        )
        nonce = str(round(datetime.now().timestamp()))
        return {
            "X-Api-Key": self.public_key,
            "X-Sign-Date": nonce,
            "X-Request-Sign": "dmar ed25519 "
            + crypto_sign(
                (method + path + "?" + urlencode(params or {}) + nonce).encode("utf-8"),
                bytes.fromhex(self.private_key),
            )[:64].hex(),
        }
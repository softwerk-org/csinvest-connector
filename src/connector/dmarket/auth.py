from datetime import datetime
from urllib.parse import urlencode

from nacl.bindings import crypto_sign


class DMarketAuth:
    """Creates DMarket authentication headers."""

    @staticmethod
    def get_headers(
        public_key: str,
        private_key: str,
        method: str,
        path: str,
        params: dict | None = None,
    ) -> dict:
        nonce = str(round(datetime.now().timestamp()))
        return {
            "X-Api-Key": public_key,
            "X-Sign-Date": nonce,
            "X-Request-Sign": "dmar ed25519 "
            + crypto_sign(
                (method + path + "?" + urlencode(params or {}) + nonce).encode("utf-8"),
                bytes.fromhex(private_key),
            )[:64].hex(),
        }

import base64


class CsDealsAuth:
    """Creates CsDeals authentication headers."""

    @staticmethod
    def get_headers(api_key: str) -> dict[str, str]:
        token = base64.b64encode(f"{api_key}:".encode("utf-8")).decode()
        return {"Authorization": f"Basic {token}"}

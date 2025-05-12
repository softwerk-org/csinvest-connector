import base64


class CsDealsAuth:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.token = base64.b64encode(f"{self.api_key}:".encode("utf-8")).decode()

    def headers(self) -> dict:
        print(self.token)
        return {"Authorization": f"Basic {self.token}"}

from src.base.api_client.base_api_client import BaseApiClient


class FrontApiClient(BaseApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: str | None = None

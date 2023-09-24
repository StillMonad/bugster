import pytest

from src.api_client.front_api_client import FrontApiClient
from src.tools.config import Config


class BaseApiTest:
    # noinspection PyAttributeOutsideInit
    @pytest.fixture(autouse=True)
    def prepare_test_session(self, request):
        self.config = Config()
        self.api_client = FrontApiClient(request.config.getoption('--front_url'))
        self.orm_session = None


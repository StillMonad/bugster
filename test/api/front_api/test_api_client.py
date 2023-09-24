from src.base.test.base_api_test import BaseApiTest


class TestApiClient(BaseApiTest):
    def test_api_client(self):
        self.api_client.get('/facts', params={'page': 1})

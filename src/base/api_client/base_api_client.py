import json
import logging
from abc import ABC
from http import HTTPStatus
from urllib.parse import urljoin
import curlify
from loguru import logger

import requests
from requests import JSONDecodeError


class HttpMethod:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"


class BaseApiClient(ABC):
    def __init__(self, host):
        self.statuses = HTTPStatus
        self.host = host
        self._http_client = requests.Session()
        self._log_level = logging.getLevelName(logging.INFO)
        self._timeout = 10

    # noinspection PyMethodMayBeStatic
    def _setup_request_params(self, *args, **kwargs) -> tuple[tuple, dict]:
        return args, kwargs

    # noinspection PyMethodMayBeStatic
    def _setup_request_handler(self, handler: str) -> str:
        return handler

    def _log_response(self, response: requests.Response, log_response: bool):
        if log_response:
            try:
                body = response.json()
                body = json.dumps(body, indent=4)
            except JSONDecodeError:
                body = response.content.decode(errors="replace")
            logger.log(self._log_level, f"response status code: {response.status_code}; response body: {body}")

    def _log_request(self, response: requests.Response, log_request: bool):
        msg = curlify.to_curl(response.request) if log_request else response.request.url
        logger.log(self._log_level, f"\n{msg}")

    def _make_request(self, method: str, handler: str, *args, **kwargs) -> requests.Response:
        log_request = kwargs.pop("log_request", True)
        log_response = kwargs.pop("log_response", True)
        timeout = kwargs.pop("timeout", self._timeout)

        param_list, param_dict = self._setup_request_params(*args, **kwargs)
        url = urljoin(self.host, self._setup_request_handler(handler))

        response = self._http_client.request(*param_list, method=method, url=url, timeout=timeout, **param_dict)

        self._log_request(response, log_request)
        self._log_response(response, log_response)

        return response

    def _make_requests(self, *args, **kwargs) -> requests.Response:
        repeat = kwargs.pop("repeat", 1)

        for _ in range(repeat):
            result = self._make_request(*args, **kwargs)
            return result

    def get(self, *args, **kwargs) -> requests.Response:
        return self._make_requests(HttpMethod.GET, *args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        return self._make_requests(HttpMethod.POST, *args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        return self._make_requests(HttpMethod.PUT, *args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        return self._make_requests(HttpMethod.PATCH, *args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        return self._make_requests(HttpMethod.DELETE, *args, **kwargs)

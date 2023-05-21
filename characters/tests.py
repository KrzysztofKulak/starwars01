import json
from unittest.mock import patch

from django.test import TestCase
from requests import Response, HTTPError

from .clients.abstract import BaseClient


def get_mock_response(expected_response: dict, expected_status_code: int = 200) -> Response:
    mock_response = Response()
    mock_response._content = json.dumps(expected_response).encode()
    mock_response.status_code = expected_status_code
    return mock_response


class TestClients(TestCase):

    def test_base_client_get_returns_response(self):
        class TestClient(BaseClient):
            BASE_URL = "https://test.url"

        test_client = TestClient()
        expected_response = {"test": "value"}
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.return_value = get_mock_response(expected_response)
            response = test_client.get("test_url")
        self.assertEqual(response, expected_response)
        mock_get.assert_called_once_with("https://test.url/test_url")

    def test_base_client_get_raises_exceptions_for_http_errors(self):
        class TestClient(BaseClient):
            BASE_URL = "https://test.url"

        test_client = TestClient()
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.return_value = get_mock_response({}, 404)
            with self.assertRaises(HTTPError):
                test_client.get("test_url")
        mock_get.assert_called_once_with("https://test.url/test_url")

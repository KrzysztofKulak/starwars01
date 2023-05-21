import json
import os
from unittest.mock import patch, call, Mock

from django.test import TestCase
from django.urls import reverse
from requests import Response, HTTPError

from .clients.abstract import BaseClient
from .clients.concrete import StarWarsSWAPIClient
from .models import Collection
from .services import fetch_characters_data


def get_mock_response(expected_response: dict, expected_status_code: int = 200) -> Response:
    mock_response = Response()
    mock_response._content = json.dumps(expected_response).encode()
    mock_response.status_code = expected_status_code
    return mock_response


class TestBaseClient(TestCase):

    def test_base_client_get_returns_response(self):
        class TestClient(BaseClient):
            BASE_URL = "https://test.url"

        test_client = TestClient()
        expected_response = {"test": "value"}
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.return_value = get_mock_response(expected_response)
            response = test_client._get("test_url")
        self.assertEqual(response, expected_response)
        mock_get.assert_called_once_with("https://test.url/test_url")

    def test_base_client_get_raises_exceptions_for_http_errors(self):
        class TestClient(BaseClient):
            BASE_URL = "https://test.url"

        test_client = TestClient()
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.return_value = get_mock_response({"detail": "Not found"}, 404)
            with self.assertRaises(HTTPError):
                test_client._get("test_url")
        mock_get.assert_called_once_with("https://test.url/test_url")


class TestStarWarsSWAPIClient(TestCase):
    def test_get_all_characters_raw(self):
        test_client = StarWarsSWAPIClient()
        mock_result = {"test": "value"}
        first_mock_response = {
            "next": "https://swapi.dev/api/people/?page=2",
            "results": [mock_result, mock_result]
        }
        another_mock_response = {"next": None, "results": [mock_result]}
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.side_effect = (
                get_mock_response(first_mock_response),
                get_mock_response(another_mock_response)
            )
            response = test_client.get_all_characters_raw()
        self.assertEqual(response, [mock_result, mock_result, mock_result])
        self.assertEqual(mock_get.mock_calls, [
            call('https://swapi.dev/api/people'),
            call('https://swapi.dev/api/people/?page=2')
        ])

    def test_get_planet(self):
        test_client = StarWarsSWAPIClient()
        expected_response = {
            "name": "Tatooine",
            "rotation_period": "23"
        }
        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.return_value = get_mock_response(expected_response)
            response = test_client.get_planet(1)
        self.assertEqual(response, expected_response)
        mock_get.assert_called_once_with("https://swapi.dev/api/planets/1")

    def test_get_all_characters(self):
        test_client = StarWarsSWAPIClient()
        expected_people_response = {
            "results": [
                {
                    "name": "Luke Skywalker",
                    "birth_year": "19BBY",
                    "homeworld": "https://swapi.dev/api/planets/1/",
                    "edited": "2014-12-20T21:17:56.891000Z"
                },
                {
                    "name": "Stachu Skywalker",
                    "birth_year": "13BBY",
                    "homeworld": "https://swapi.dev/api/planets/2/",
                    "edited": "2014-12-20T21:17:50.309000Z"
                }
            ],
            "next": None
        }
        expected_planet_1_response = {
            "name": "Tatooine",
            "rotation_period": "23"
        }
        expected_planet_2_response = {
            "name": "Alderaan",
            "rotation_period": "24"
        }

        with patch("characters.clients.abstract.requests.get") as mock_get:
            mock_get.side_effect = [
                get_mock_response(expected_people_response),
                get_mock_response(expected_planet_1_response),
                get_mock_response(expected_planet_2_response)
            ]
            response = test_client.get_all_characters()
        self.assertEqual(response,
                         [
                             {
                                 "name": "Luke Skywalker",
                                 "birth_year": "19BBY",
                                 "homeworld": "Tatooine",
                                 "date": "2014-12-20"
                             },
                             {
                                 "name": "Stachu Skywalker",
                                 "birth_year": "13BBY",
                                 "homeworld": "Alderaan",
                                 "date": "2014-12-20"
                             }
                         ]
                         )
        self.assertEqual(mock_get.mock_calls, [
            call('https://swapi.dev/api/people'),
            call('https://swapi.dev/api/planets/1'),
            call('https://swapi.dev/api/planets/2')
        ])


class TestServices(TestCase):
    def test_fetch_characters_data(self):
        mock_star_wars_service = Mock()
        mock_return_value = [
            {
                "name": "Luke Skywalker",
                "birth_year": "19BBY",
                "homeworld": "Tatooine",
                "date": "2014-12-20"
            },
            {
                "name": "Stachu Skywalker",
                "birth_year": "13BBY",
                "homeworld": "Alderaan",
                "date": "2014-12-20"
            }
        ]
        mock_star_wars_service.get_all_characters.return_value = mock_return_value
        fetch_characters_data(mock_star_wars_service)
        collection = Collection.objects.all().first()
        self.assertEqual(Collection.objects.all().count(), 1)
        self.assertEqual(collection.csv_file.name, f"characters/{collection.id}.csv")
        os.remove(f"media/characters/{collection.id}.csv")


class CollectionViewsTestCase(TestCase):
    def test_fetch_collection_post(self):
        mock_star_wars_service = Mock()
        mock_star_wars_service.get_all_characters.return_value = [
            {
                "name": "Luke Skywalker",
                "birth_year": "19BBY",
                "homeworld": "Tatooine",
                "date": "2014-12-20"
            },
            {
                "name": "Stachu Skywalker",
                "birth_year": "13BBY",
                "homeworld": "Alderaan",
                "date": "2014-12-20"
            }
        ]
        response = self.client.post(reverse('fetch_collection'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('collections_list'))

        collection = Collection.objects.all().first()
        os.remove(f"media/characters/{collection.id}.csv")

    def test_collections_list(self):
        Collection.objects.create()
        Collection.objects.create()

        response = self.client.get(reverse('collections_list'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['collections']), 2)

    def test_collection_details(self):
        """
        IMPROVEMENT IDEA:
        mock_star_wars_service could be a fixture
        """
        mock_star_wars_service = Mock()
        mock_return_value = [
            {
                "name": "Luke Skywalker",
                "birth_year": "19BBY",
                "homeworld": "Tatooine",
                "date": "2014-12-20"
            },
            {
                "name": "Stachu Skywalker",
                "birth_year": "13BBY",
                "homeworld": "Alderaan",
                "date": "2014-12-20"
            }
        ]
        mock_star_wars_service.get_all_characters.return_value = mock_return_value
        fetch_characters_data(mock_star_wars_service)

        collection = Collection.objects.all().first()

        collection.csv_file = f'characters/{collection.id}.csv'
        collection.save()

        response = self.client.get(reverse('collection_details', kwargs={'collection_id': collection.id}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['collection'], str(collection))
        self.assertEqual(len(response.context['headers']), len(mock_return_value[0].keys()))
        self.assertEqual(response.context['id'], collection.id)
        self.assertEqual(response.context['next_limit'], 20)

        os.remove(f"media/characters/{collection.id}.csv")
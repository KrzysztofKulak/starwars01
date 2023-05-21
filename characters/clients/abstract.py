import abc
import logging
from json import JSONDecodeError

import requests
from requests import HTTPError

from starwarsarchive.starwarsarchive import settings

logger = logging.getLogger(__name__)


class BaseClient(abc.ABC):
    BASE_URL: str

    def get(self, url: str) -> dict:
        path = f"{self.BASE_URL}/{url}"
        logger.info(f"Making a [GET] request to {path}.")
        try:
            response = requests.get(path)
            response.raise_for_status()
        except HTTPError as exc:
            logger.error(f"An HTTP error has occurred when calling {path}: {exc}")
            raise
        except JSONDecodeError:
            logger.error(f"Cannot parse response from {path}.")
            raise
        return response.json()


class StarWarsAbstractClient(BaseClient):
    BASE_URL = settings.SWAPI_URL

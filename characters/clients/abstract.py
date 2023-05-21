import abc
import logging
from json import JSONDecodeError

import requests
from requests import HTTPError

logger = logging.getLogger(__name__)


class BaseClient(abc.ABC):
    BASE_URL: str

    def _get(self, url: str, use_base_url: bool = True) -> dict:
        if use_base_url:
            path = f"{self.BASE_URL}/{url}"
        else:
            path = url
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


class StarWarsClient(BaseClient):

    @abc.abstractmethod
    def get_all_characters(self) -> list[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_planet(self, id: int) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_characters_parsed(self) -> list[dict]:
        raise NotImplementedError

import abc
import logging
from json import JSONDecodeError

import requests
from requests import HTTPError

logger = logging.getLogger(__name__)


class BaseClient(abc.ABC):
    def _get(self, url: str) -> dict:
        logger.info(f"Making a [GET] request to {url}.")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as exc:
            logger.error(f"An HTTP error has occurred when calling {url}: {exc}")
            raise
        except JSONDecodeError:
            logger.error(f"Cannot parse response from {url}.")
            raise
        return response.json()


class StarWarsClient(BaseClient):
    @abc.abstractmethod
    def get_all_characters(self) -> list[dict]:
        raise NotImplementedError

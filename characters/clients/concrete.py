import dateutil.parser as date_parser

from characters.clients.abstract import StarWarsClient
from starwarsarchive import settings


class StarWarsSWAPIClient(StarWarsClient):
    FIELDS_TO_BE_OMITTED = [
        "films", "species", "url", "created", "edited", "vehicles", "starships"
    ]
    BASE_URL = settings.SWAPI_URL

    def get_all_characters_raw(self) -> list[dict]:
        url = f"{self.BASE_URL}/people"
        characters = []
        while url:
            response = self._get(url)
            url = response["next"]
            characters.extend(response["results"])
        return characters

    def get_all_planets(self) -> list[dict]:
        url = f"{self.BASE_URL}/planets"
        planets = []
        while url:
            response = self._get(url)
            url = response["next"]
            planets.extend(response["results"])
        return planets

    def get_all_characters(self) -> list[dict]:
        characters = self.get_all_characters_raw()
        planets = {planet["url"]: planet for planet in self.get_all_planets()}
        for character in characters:
            if character["homeworld"] != "n/a":
                character["homeworld"] = planets[character["homeworld"]]["name"]
            character["date"] = date_parser.isoparse(character["edited"]).strftime("%Y-%m-%d")
            for key in self.FIELDS_TO_BE_OMITTED:
                character.pop(key, None)
        return characters

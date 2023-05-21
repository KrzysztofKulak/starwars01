from characters.clients.abstract import StarWarsClient
from starwarsarchive import settings


class StarWarsSWAPIClient(StarWarsClient):
    BASE_URL = settings.SWAPI_URL

    def get_all_characters(self) -> list[dict]:
        url = f"{self.BASE_URL}/people"
        characters = []
        while url:
            response = self._get(url, use_base_url=False)
            url = response["next"]
            characters.extend(response["results"])
        return characters

    def get_planet(self, id: int) -> dict:
        url = f"planets/{id}"
        return self._get(url)

    def get_all_characters_with_planets(self) -> list[dict]:
        characters = self.get_all_characters()
        planets = {}
        for character in characters:
            if character["homeworld"] != "n/a":
                if not planets.get(character["homeworld"]):
                    planets[character["homeworld"]] = self.get_planet(
                        character["homeworld"].split("/")[-2]
                    )
                character["homeworld"] = planets[character["homeworld"]]["name"]
        return characters

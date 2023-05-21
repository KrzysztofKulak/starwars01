from characters.clients.abstract import StarWarsClient
from starwarsarchive import settings


class StarWarsSWAPIClient(StarWarsClient):
    FIELDS_TO_BE_OMITTED = [
        "films", "species", "url", "created", "edited", "vehicles", "starships"
    ]
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

    def get_all_characters_parsed(self) -> list[dict]:
        characters = self.get_all_characters()
        planets = {}
        for character in characters:
            """ 
            IMPROVEMENT IDEA:
            This could be generalized to map all link-fields to a name of the resource, 
            mapping of the field from the target resource to be used could look like:
            {
            "homeworld": "name",
            "films": "title"
            }
            and so on, the fact that some link-fields are lists would have to be taken 
            into consideration.
            """
            if character["homeworld"] != "n/a":
                if not planets.get(character["homeworld"]):
                    planets[character["homeworld"]] = self.get_planet(
                        character["homeworld"].split("/")[-2]
                    )
                character["homeworld"] = planets[character["homeworld"]]["name"]
            character["date"] = character["edited"]
            for key in self.FIELDS_TO_BE_OMITTED:
                character.pop(key, None)
        return characters

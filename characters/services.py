import os
from uuid import UUID

import petl
from django.core.files import File
from petl import FieldSelectionError

from characters.clients.abstract import StarWarsClient
from characters.models import Collection


def fetch_characters_data(star_wars_client: StarWarsClient):
    collection = Collection()
    """
    IMPROVEMENT IDEA:
    new Collection instance could be saved with a placeholder value
    and returned to a rendered list, but SWAPI calling and csv saving 
    operation could be moved into a Celery task to be run asynchronously
    by a Celery worker, where instance would be updated with the info
    the newly created csv file.
    """
    characters = star_wars_client.get_all_characters()
    characters_table = petl.fromdicts(characters)
    temp_csv_file = f"{collection.id}.csv"
    petl.tocsv(characters_table, temp_csv_file)
    with open(temp_csv_file, 'rb') as f:
        collection.csv_file = File(f)
        collection.save()
    os.remove(temp_csv_file)


class InvalidColumnNameException(Exception):
    pass


def count_values(collection_id: UUID, columns: list[str]) -> list[dict]:
    collection = Collection.objects.get(pk=collection_id)
    items = petl.fromcsv(collection.csv_file.path)
    try:
        value_counts = list(petl.dicts(petl.valuecounts(items, *columns)))
    except FieldSelectionError:
        raise InvalidColumnNameException()
    return value_counts

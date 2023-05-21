import os

import petl
from django.core.files import File

from characters.clients.concrete import StarWarsSWAPIClient
from characters.models import Collection


def fetch_characters_data():
    collection = Collection()
    """
    IMPROVEMENT IDEA:
    new Collection instance could be saved with a placeholder value
    and returned to a rendered list, but SWAPI calling and csv saving 
    operation could be moved into a Celery task to be run asynchronously
    by a Celery worker, where instance would be updated with the info
    the newly created csv file.
    """
    characters = StarWarsSWAPIClient().get_all_characters_parsed()
    characters_table = petl.fromdicts(characters)
    temp_csv_file = f"{collection.id}.csv"
    petl.tocsv(characters_table, temp_csv_file)
    with open(temp_csv_file, 'rb') as f:
        collection.csv_file = File(f)
        collection.save()
    os.remove(temp_csv_file)
import os

import petl
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from characters.clients.concrete import StarWarsSWAPIClient
from characters.models import Collection


@csrf_exempt
def collections(request):
    if request.method == "POST":
        characters = StarWarsSWAPIClient().get_all_characters_with_planets()
        characters_table = petl.fromdicts(characters)
        collection = Collection()
        temp_csv_file = f"{collection.id}.csv"
        petl.tocsv(characters_table, temp_csv_file)
        with open(temp_csv_file, 'rb') as f:
            collection.csv_file = File(f)
            collection.save()
        os.remove(temp_csv_file)
    collections = Collection.objects.all()
    return JsonResponse(
        {
            'results': [
                f"{collection.id} {collection.created_at}" for collection in collections
            ]
        },
        status=200)

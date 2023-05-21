import os

import petl
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from characters.models import Collection
from characters.services import fetch_characters_data


def fetch_collection(request):
    if request.method == "POST":
        fetch_characters_data()
        return redirect('collection_list')

def collection_list(request):
    collections = Collection.objects.order_by('-created_at').all()
    return render(
        request,
        "collection_list.html",
        {
            "collections": [
                {"id": collection.id, "string": str(collection)}
                for collection in collections
            ]
        }
    )


def collection_details(request, collection_id):
    collection = Collection.objects.get(pk=collection_id)
    items = petl.dicts(petl.fromcsv(collection.csv_file.path))
    return render(
        request,
        "collection_details.html",
        {
            "collection": str(collection),
            "headers": items[0].keys() if items else [],
            "items": items
        }
    )

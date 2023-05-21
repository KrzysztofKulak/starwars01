import petl
from django.shortcuts import render, redirect

from characters.clients.abstract import StarWarsClient
from characters.models import Collection
from characters.services import fetch_characters_data

"""
IMPROVEMENT IDEA:
1. adding DRF and exposing an API to be consumed by e.g. 
React or mobile app, or some other server-side service
2. adding error handlers for StarWarsClient originating
exceptions to handle service being down 
"""

def fetch_collection(request, star_wars_service_client: StarWarsClient):
    if request.method == "POST":
        fetch_characters_data(star_wars_service_client)
        return redirect('collections_list')


def collections_list(request):
    collections = Collection.objects.order_by('-created_at').all()
    return render(
        request,
        "collections_list.html",
        {
            "collections": [
                {"id": collection.id, "string": str(collection)}
                for collection in collections
            ]
        }
    )


def collection_details(request, collection_id):
    limit = int(request.GET.get('limit', 10))
    collection = Collection.objects.get(pk=collection_id)
    if limit != -1:
        items = petl.dicts(petl.fromcsv(collection.csv_file.path).head(limit))
    else:
        items = petl.dicts(petl.fromcsv(collection.csv_file.path))
    return render(
        request,
        "collection_details.html",
        {
            "collection": str(collection),
            "headers": items[0].keys() if items else [],
            "items": items,
            "id": collection.id,
            "next_limit": limit + 10,
        }
    )

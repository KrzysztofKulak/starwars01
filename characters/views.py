from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from characters.clients.concrete import StarWarsSWAPIClient
from characters.models import Collection


@csrf_exempt
def collections(request):
    collections = Collection.objects.all()
    return JsonResponse(
        {
            'results': [
                f"{collection.id} {collection.created_at}" for collection in collections
            ]
        }
        , status=200)

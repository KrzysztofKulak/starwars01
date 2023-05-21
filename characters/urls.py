from django.urls import path

from . import views
from .clients.concrete import StarWarsSWAPIClient

star_wars_client = StarWarsSWAPIClient()

"""
IMPROVEMENT IDEA:
star_wars_client could be injected more elegantly, e.g. using injector library.
Still: in it's current form the data source is strongly decoupled from the representation.
"""
urlpatterns = [
    path('fetch', views.fetch_collection, {"star_wars_service_client": star_wars_client}, name="fetch_collection"),
    path('', views.collections_list, name="collections_list"),
    path('<uuid:collection_id>', views.collection_details, name="collection_details"),
    path('<uuid:collection_id>/counts', views.collection_value_count, name="collection_value_count")
]

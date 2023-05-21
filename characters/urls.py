from django.urls import path

from . import views

urlpatterns = [
    path('fetch', views.fetch_collection, name="fetch_collection"),
    path('', views.collection_list, name="collection_list"),
    path('<uuid:collection_id>', views.collection_details, name="collection_details")
]

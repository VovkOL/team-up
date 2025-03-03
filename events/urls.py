from django.urls import path
from .views import (
    index,
    LocationListView,
)


app_name = "events"

urlpatterns = [
    path("", index, name="index"),
    path("locations/", LocationListView.as_view(), name="location-list"),
]

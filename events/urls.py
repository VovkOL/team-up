from django.urls import path
from .views import (
    index,
    LocationListView, LocationDetailView, LocationCreateView,
)


app_name = "events"

urlpatterns = [
    path("", index, name="index"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("location/create/", LocationCreateView.as_view(), name="location-create"),
]

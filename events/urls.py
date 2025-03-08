from django.urls import path
from .views import (
    index,
    LocationListView,
    LocationDetailView,
    LocationCreateView,
    LocationUpdateView,
    SportTypeCreateView, SportTypeListView, SportTypeDetailView, SportTypeUpdateView, AthleteCreateView,
)


app_name = "events"

urlpatterns = [
    path("", index, name="index"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("location/create/", LocationCreateView.as_view(), name="location-create"),
    path("location/<int:pk>/update/", LocationUpdateView.as_view(), name="location-update"),
    path("sport-type/create/", SportTypeCreateView.as_view(), name="sport-type-create"),
    path("sport-types/", SportTypeListView.as_view(), name="sport-type-list"),
    path("sport-type/<int:pk>/", SportTypeDetailView.as_view(), name="sport-type-detail"),
    path("sport-type/<int:pk>/update/", SportTypeUpdateView.as_view(), name="sport-type-update"),
    path("athlete/create/", AthleteCreateView.as_view(), name="athlete-create"),
]

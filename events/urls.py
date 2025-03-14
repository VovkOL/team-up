from django.urls import path
from .views import (
    index,
    LocationListView,
    LocationDetailView,
    LocationCreateView,
    LocationUpdateView,
    SportTypeCreateView,
    SportTypeListView,
    SportTypeDetailView,
    SportTypeUpdateView,
    AthleteCreateView,
    AthleteListView,
    AthleteDetailView,
    AthleteUpdateView,
    AddFriendView,
    RemoveFriendView,
    TrainingSessionCreateView,
    TrainingSessionDetailView,
    JoinSessionView,
    LeaveSessionView,
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
    path("athletes/", AthleteListView.as_view(), name="athlete-list"),
    path("athlete/<int:pk>/", AthleteDetailView.as_view(), name="athlete-detail"),
    path("athlete/<int:pk>/update/", AthleteUpdateView.as_view(), name="athlete-update"),
    path("athlete/<int:pk>/add-friend/", AddFriendView.as_view(), name='add-friend'),
    path("athlete/<int:pk>/remove-friend/", RemoveFriendView.as_view(), name='remove-friend'),
    path("training-session/create/", TrainingSessionCreateView.as_view(), name="training-session-create"),
    path("training-session/<int:pk>/detail/", TrainingSessionDetailView.as_view(), name="training-session-detail"),
    path('training-session/<int:pk>/join/', JoinSessionView.as_view(), name='join-session'),
    path('training-session/<int:pk>/leave/', LeaveSessionView.as_view(), name='leave-session'),
]

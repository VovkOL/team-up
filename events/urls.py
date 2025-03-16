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
    TrainingSessionListView,
    TrainingSessionUpdateView,
)


app_name = "events"

urlpatterns = [
    path("", index, name="index"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("locations/create/", LocationCreateView.as_view(), name="location-create"),
    path("locations/<int:pk>/update/", LocationUpdateView.as_view(), name="location-update"),
    path("sport-types/create/", SportTypeCreateView.as_view(), name="sport-type-create"),
    path("sport-types/", SportTypeListView.as_view(), name="sport-type-list"),
    path("sport-types/<int:pk>/", SportTypeDetailView.as_view(), name="sport-type-detail"),
    path("sport-types/<int:pk>/update/", SportTypeUpdateView.as_view(), name="sport-type-update"),
    path("athletes/create/", AthleteCreateView.as_view(), name="athlete-create"),
    path("athletes/", AthleteListView.as_view(), name="athlete-list"),
    path("athletes/<int:pk>/", AthleteDetailView.as_view(), name="athlete-detail"),
    path("athletes/<int:pk>/update/", AthleteUpdateView.as_view(), name="athlete-update"),
    path("athletes/<int:pk>/add-friend/", AddFriendView.as_view(), name="add-friend"),
    path("athletes/<int:pk>/remove-friend/", RemoveFriendView.as_view(), name="remove-friend"),
    path("training-sessions/create/", TrainingSessionCreateView.as_view(), name="training-session-create"),
    path("training-sessions/<int:pk>/detail/", TrainingSessionDetailView.as_view(), name="training-session-detail"),
    path("training-sessions/<int:pk>/join/", JoinSessionView.as_view(), name="join-session"),
    path("training-sessions/<int:pk>/leave/", LeaveSessionView.as_view(), name="leave-session"),

]

from django.shortcuts import render

from events.models import Location, SportType, Athlete, TrainingSession


def index(request):
    num_locations = Location.objects.count()
    num_sport_types = SportType.objects.count()
    num_athletes = Athlete.objects.count()
    num_training_sessions = TrainingSession.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_locations": num_locations,
        "num_sport_types": num_sport_types,
        "num_athletes": num_athletes,
        "num_training_sessions": num_training_sessions,
        "num_visits": num_visits + 1,
    }

    return render(request, "events/index.html", context=context)

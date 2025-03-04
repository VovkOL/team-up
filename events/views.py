from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from events.forms import LocationSearchForm
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


class LocationListView(generic.ListView):
    model = Location
    context_object_name = "location_list"
    template_name = "events/location_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = LocationSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = LocationSearchForm(self.request.GET)
        if form.is_valid():
            return Location.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class LocationDetailView(generic.DetailView):
    model = Location

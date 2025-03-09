from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.contrib import messages

from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from events.forms import LocationSearchForm, SportTypeSearchForm, AthleteCreationForm, AthleteSearchForm
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


class LocationCreateView(generic.CreateView):
    model = Location
    success_url = reverse_lazy("events:location-list")
    template_name = "events/location_form.html"
    fields = "__all__"


class LocationUpdateView(generic.UpdateView):
    model = Location
    success_url = reverse_lazy("events:location-list")
    template_name = "events/location_form.html"
    fields = "__all__"


class SportTypeCreateView(generic.CreateView):
    model = SportType
    success_url = reverse_lazy("events:sport-type-list")
    template_name = "events/sport-type_form.html"
    fields = "__all__"


class SportTypeListView(generic.ListView):
    model = SportType
    context_object_name = "sport_type_list"
    template_name = "events/sport-type_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context =super(SportTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SportTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = LocationSearchForm(self.request.GET)
        if form.is_valid():
            return SportType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class SportTypeDetailView(generic.DetailView):
    model = SportType
    context_object_name = "sport_type"
    template_name = "events/sport-type_detail.html"


class SportTypeUpdateView(generic.UpdateView):
    model = SportType
    success_url = reverse_lazy("events:sport-type-list")
    context_object_name = "sport_type"
    template_name = "events/sport-type_form.html"
    fields = "__all__"


class AthleteCreateView(generic.CreateView):
    model = Athlete
    success_url = reverse_lazy('events:athlete-list')
    template_name = "events/athlete_form.html"
    form_class = AthleteCreationForm

    def form_valid(self, form):
        return super().form_valid(form)


class AthleteListView(generic.ListView):
    model = Athlete
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AthleteListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = AthleteSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = AthleteSearchForm(self.request.GET)
        if form.is_valid():
            return Athlete.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

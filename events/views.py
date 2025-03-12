from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib import messages

from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from events.forms import LocationSearchForm, SportTypeSearchForm, AthleteCreationForm, AthleteSearchForm, \
    AthleteUpdateForm
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


class LocationListView(LoginRequiredMixin, generic.ListView):
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


class LocationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Location


class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    success_url = reverse_lazy("events:location-list")
    template_name = "events/location_form.html"
    fields = "__all__"


class LocationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Location
    success_url = reverse_lazy("events:location-list")
    template_name = "events/location_form.html"
    fields = "__all__"


class SportTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = SportType
    success_url = reverse_lazy("events:sport-type-list")
    template_name = "events/sport-type_form.html"
    fields = "__all__"


class SportTypeListView(LoginRequiredMixin, generic.ListView):
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


class SportTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = SportType
    context_object_name = "sport_type"
    template_name = "events/sport-type_detail.html"


class SportTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SportType
    success_url = reverse_lazy("events:sport-type-list")
    context_object_name = "sport_type"
    template_name = "events/sport-type_form.html"
    fields = "__all__"


class AthleteCreateView(generic.CreateView):
    model = Athlete
    success_url = reverse_lazy('events:athlete-list')
    template_name = "events/athlete_sign_up.html"
    form_class = AthleteCreationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

        return response



class AthleteListView(LoginRequiredMixin, generic.ListView):
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


class AthleteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Athlete
    template_name = "events/athlete_detail.html"


class AthleteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Athlete
    success_url = reverse_lazy('events:athlete-list')
    template_name = "events/athlete_update.html"
    form_class = AthleteUpdateForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.pk != self.request.user.pk:
            raise Http404("You can only update your own profile")
        return obj


class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        athlete = get_object_or_404(Athlete, pk=pk)
        if request.user != athlete:
            athlete.friends.add(request.user)
            messages.success(request, f"You have added {athlete.username} to your friends!")
        else:
            messages.error(request, "You cannot add yourself as a friend.")
        return redirect('events:athlete-detail', pk=pk)


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        athlete = get_object_or_404(Athlete, pk=pk)
        if request.user != athlete and request.user in athlete.friends.all():
            athlete.friends.remove(request.user)
            messages.success(request, f"You have removed {athlete.username} from your friends!")
        else:
            messages.error(request, "You cannot remove yourself or this user is not your friend.")
        return redirect('events:athlete-detail', pk=pk)

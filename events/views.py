from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages

from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from events.forms import LocationSearchForm, SportTypeSearchForm, AthleteCreationForm, AthleteSearchForm, \
    AthleteUpdateForm, TrainingSessionForm, TrainingSessionSearchForm
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


class TrainingSessionCreateView(LoginRequiredMixin, generic.CreateView):
    model = TrainingSession
    template_name = "events/training-session_form.html"
    form_class = TrainingSessionForm

    def get_success_url(self):
        return reverse("events:training-session-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.host = self.request.user
        messages.success(self.request, "Training session created successfully!")
        return super().form_valid(form)


class TrainingSessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = TrainingSession
    context_object_name = "training_session"
    template_name = "events/training-session_detail.html"


class JoinSessionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        if session.athletes.count() < session.max_athletes:
            session.athletes.add(request.user)
            messages.success(request, "You have successfully joined the training session!")
        else:
            messages.error(request, "The session is already full.")
        return redirect('events:training-session-detail', pk=pk)


class LeaveSessionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        if request.user in session.athletes.all():
            session.athletes.remove(request.user)
            messages.success(request, "You have left the training session.")
        else:
            messages.error(request, "You are not a participant in this session.")
        return redirect('events:training-session-detail', pk=pk)


class TrainingSessionListView(LoginRequiredMixin, generic.ListView):
    model = TrainingSession
    template_name = "events/training-session_list.html"
    context_object_name = "training_sessions"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TrainingSessionListView, self).get_context_data(**kwargs)
        sport_type = self.request.GET.get("sport_type", "")
        context["search_form"] = TrainingSessionSearchForm(
            initial={"sport_type": sport_type}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TrainingSessionSearchForm(self.request.GET)
        if form.is_valid():
            return TrainingSession.objects.filter(
                sport_type__name__icontains=form.cleaned_data["sport_type"]
            )
        return queryset

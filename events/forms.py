from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from events.models import Athlete, Location


class LocationSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by city name"}),
    )


class SportTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by sport type"}),
    )


class LocationFilterMixin:
    def get_filtered_locations(self):
        unique_locations = {}
        for location in Location.objects.all().order_by("name", "id"):
            if location.name not in unique_locations:
                unique_locations[location.name] = location.pk

        return Location.objects.filter(pk__in=unique_locations.values()).order_by("name")


class AthleteCreationForm(UserCreationForm, LocationFilterMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["location"].queryset = self.get_filtered_locations()

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label="Select a location",
    )

    class Meta:
        model = Athlete
        fields = ("username", "first_name", "last_name", "location", "password1", "password2")


class AthleteSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class AthleteUpdateForm(forms.ModelForm, LocationFilterMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["location"].queryset = self.get_filtered_locations()

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label="Select a location",
    )


    class Meta:
        model = Athlete
        fields = ["username", "first_name", "last_name", "location"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Athlete.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

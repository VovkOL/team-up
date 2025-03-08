from django import forms
from django.contrib.auth.forms import UserCreationForm

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


class AthleteCreationForm(UserCreationForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.values_list("name", flat=True).distinct(),
        required=False,
        empty_label="Select a location",
    )

    class Meta(UserCreationForm.Meta):
        model = Athlete
        fields = (
            "username",
            "first_name",
            "last_name",
            "location",
            "friends",
            "password1",
            "password2",
        )


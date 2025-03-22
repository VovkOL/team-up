from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return f"{self.name} ({self.address})"

    def get_absolute_url(self):
        return reverse("events:location-detail", args=[str(self.id)])


class SportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    min_athletes = models.PositiveIntegerField(blank=True, null=True)
    max_athletes = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events:sport-type-detail", args=[str(self.id)])

class Athlete(AbstractUser):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    class Meta:
        verbose_name = "athlete"
        verbose_name_plural = "athletes"

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("events:athlete-detail", kwargs={"pk": self.pk})


class TrainingSession(models.Model):
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    host = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="hosted_sessions")
    athletes = models.ManyToManyField(Athlete,related_name="joined_sessions", blank=True)
    max_athletes = models.PositiveIntegerField(
        default=2,
        validators=[
            MinValueValidator(2, message="Max athletes cannot be less than 2."),
            MaxValueValidator(50, message="Max athletes cannot be more than 50."),
        ]
    )
    description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ("date_time", )

    def __str__(self):
        return f"{self.sport_type.name} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    def available_slots(self):
        return self.max_athletes - self.athletes.count()

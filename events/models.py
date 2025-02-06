from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class SportType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name

class Athlete(AbstractUser):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    friends = models.ManyToManyFields("self", symmetrical=True, blank=True)

    class Meta:
        verbose_name = "athlete"
        verbose_name_plural = "athletes"

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("events:athlete-detail", kwargs={"pk": self.pk})

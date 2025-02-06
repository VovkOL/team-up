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

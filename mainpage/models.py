from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


class Job(models.Model):
    title = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    apply_date = models.DateField(default=timezone.localdate)
    description = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-apply_date', 'title']

    def __str__(self):
        return f"{self.title} with {self.employer}. Applied on {self.apply_date}"

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})

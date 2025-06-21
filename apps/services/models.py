from django.db import models

from apps.sectors.models import Sector


class Service(models.Model):
    name_ar = models.CharField(max_length=255)
    description_ar = models.TextField()
    name_en = models.CharField(max_length=255)
    description_en = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    sectors = models.ManyToManyField(Sector, related_name='services')

    def __str__(self):
        return f"{self.name_ar} / {self.name_en}"
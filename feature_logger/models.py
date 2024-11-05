from django.db import models
from django.utils import timezone


class FeatureLog(models.Model):
    """ Information around a feature logs """
    data = models.JSONField(default=dict, blank=dict)
    model_name = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

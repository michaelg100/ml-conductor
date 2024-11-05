from django.db import models
from django.utils import timezone


class ModelMetadata(models.Model):
    """ Information around a ML model """
    model_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)


class ModelExpirementMetrics(models.Model):
    """ Information around training expirement for a ML model """
    model = models.ForeignKey(ModelMetadata, on_delete=models.CASCADE)
    metrics = models.JSONField(default=dict, blank=dict, null=True)
    feature_set = models.JSONField(default=list, blank=list, null=True)
    target_field = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
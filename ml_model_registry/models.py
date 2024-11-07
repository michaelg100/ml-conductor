from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ModelMetadata(models.Model):
    """ Information around a ML model """
    class ModelDataType(models.TextChoices):
        TENSORFLOW = "TENSORFLOW", _("Tensorflow")
        PYTORCH = "PYTORCH", _("Pytorch")
        SCIKIT = "SCIKIT", _("Scikit")
    model_type = models.CharField(max_length=250, choices=ModelDataType.choices, default=ModelDataType.SCIKIT)
    # store as [<feature store>: [<feature>,...],...]
    feature_set = models.JSONField(default=dict, blank=dict, null=True)
    model_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    # api
    api_url = models.CharField(max_length=500, null=True, blank=True)


class ModelExpirementMetrics(models.Model):
    """ Information around training expirement for a ML model """
    model = models.ForeignKey(ModelMetadata, on_delete=models.CASCADE)
    metrics = models.JSONField(default=dict, blank=dict, null=True)
    target_field = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
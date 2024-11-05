from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FeatureStore(models.Model):
    """ Information around a feature store """
    feature_store_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)


class FeatureMetadata(models.Model):
    """ Infromation on each feature and the feature store it is apart of """

    class FeatureDataType(models.TextChoices):
        STRING = "STRING", _("String")
        INT = "INT", _("Integer")
        FLOAT = "FLOAT", _("Float")
        ARRAY_STRING = "ARRAY_STRING", _("ArrayString")
        ARRAY_INT = "ARRAY_INT", _("ArrayInt")
        ARRAY_FLOAT = "ARRAY_FLOAT", _("ArrayFloat")

    feature_name = models.CharField(max_length=250)
    datatype = models.CharField(max_length=250, choices=FeatureDataType.choices, default=FeatureDataType.STRING)
    feature_store = models.ForeignKey(FeatureStore, on_delete=models.PROTECT)
    feature_description = models.TextField(blank=True, null=True)
    data_source = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("feature_name", "feature_store")


class Features(models.Model):
    """ Stores all the feature values """
    features = models.JSONField(default=dict, blank=dict)
    feature_store = models.ForeignKey(FeatureStore, on_delete=models.PROTECT)
    entity_id = models.BigIntegerField()
    last_modified = models.DateTimeField(auto_now=True)
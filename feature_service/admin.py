from django.contrib import admin

from feature_service.models import *

admin.site.register(FeatureMetadata)
admin.site.register(FeatureStore)
admin.site.register(Features)

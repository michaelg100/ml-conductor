from django.db import transaction
from http import HTTPStatus
from ninja.errors import HttpError

from ml_model_registry.models import *
from ml_model_registry.types import *


class ModelRegistryService:

    @classmethod
    def upload_model_expirement(cls, expirement: ModelExpirementInsertT) -> ModelExpirementMetrics:
        with transaction.atomic():
            try:
                # create model
                ml_model = ModelMetadata.objects.create(
                    model_name=expirement.model_name,
                    location=expirement.location,
                    feature_set=expirement.feature_set,
                    description=expirement.model_description
                )
            except:
                raise HttpError(
                    status_code=HTTPStatus.BAD_REQUEST.value,
                    message=f"Make sure the model name and location are unique from existing"
                )
            # create expirement
            try:
                expirement_model = ModelExpirementMetrics.objects.create(
                    model=ml_model,
                    metrics=expirement.metrics,
                    target_field=expirement.target_field,
                    description=expirement.expirement_description
                )
            except Exception as e:
                raise HttpError(
                    status_code=HTTPStatus.BAD_REQUEST.value,
                    message=f"{e}"
                )
            return expirement_model

    @classmethod
    def add_serving_api_url(cls, model_name: str, api_url: str) -> str:
        model = ModelMetadata.objects.filter(model_name=model_name).first()
        if not model:
            return "No model exists in ModelMetadata table with the name {model_name}"
        model.api_url = api_url
        model.save(update_fields=['api_url'])
        return f"Updated the model's (name: {model_name}) API URL"
from typing import Dict, List

from ml_model_registry.models import *


def create_model(
    model_name: str,
    location: str,
    feature_set: Dict[str, List[str]],
    description: str,
    api_url: str
) -> ModelMetadata:
    return ModelMetadata.objects.get_or_create(
        model_name=model_name,
        location=location,
        feature_set=feature_set,
        description=description,
        api_url=api_url
    )
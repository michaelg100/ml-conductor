from feature_service.models import *


def create_feature_store(feature_store: str):
    fixture, _ = FeatureStore.objects.get_or_create(
        feature_store_name=feature_store,
        description="test feature store description",
    )
    return fixture

def create_feature_metadata(feature_name: str, feature_store: str):
    feature_store = create_feature_store(feature_store)
    fixture, _ = FeatureMetadata.objects.get_or_create(
        name=feature_name,
        feature_store=feature_store,
        defaults={
            "datatype": "STRING",
            "feature_description": "test feature metadata description",
            "data_source": "no data source found",
        }
    )
    return fixture

def create_empty_feature(feature_store: str, entity_id: int = 1):
    fixture, _ = Features.objects.get_or_create(
        feature_store=feature_store,
        entity_id=entity_id
    )
    return fixture

def create_feature(feature_store: str, data: dict, entity_id: int = 1):
    feature_store = create_feature_store(feature_store)
    fixture = create_empty_feature(feature_store=feature_store, entity_id=entity_id)
    fixture.features = data
    fixture.save(update_fields=['features'])
    return fixture
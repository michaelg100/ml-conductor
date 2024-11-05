from django.db import transaction
from http import HTTPStatus
from ninja.errors import HttpError
from typing import Dict

from feature_service.models import *
from feature_service.types import *


class FeatureService:

    @classmethod
    def _check_feature_store(cls, feature_store_name: str) -> FeatureStore:
        feature_store = FeatureStore.objects.filter(feature_store_name=feature_store_name).first()
        if not feature_store:
            raise HttpError(
                status_code=HTTPStatus.BAD_REQUEST.value,
                message=f"The feature store: {feature_store_name} is not register in FeatureStore table."
            )
        return feature_store
    
    @classmethod
    def _match_db_datatype_to_python_datatype(cls, datatype: str) -> str:
        match datatype:
            case "STRING":
                return str|None
            case "INT":
                return int|None
            case "FLOAT":
                return float|None
            case "ARRAY_STRING":
                return list[str|None]|None
            case "ARRAY_INT":
                return list[int|None]|None
            case "ARRAY_FLOAT":
                return list[float|None]|None
            case _:
                raise HttpError(
                    status_code=HTTPStatus.BAD_REQUEST.value,
                    message=f"The datatype: {datatype} is not allowed."
                )


    @classmethod
    def _match_datatype(cls, datatype: int) -> str:
        match datatype:
            case FeatureTypes.string:
                return "STRING"
            case FeatureTypes.integer:
                return "INT"
            case FeatureTypes.float:
                return "FLOAT"
            case FeatureTypes.array_integer:
                return "ARRAY_STRING"
            case FeatureTypes.array_string:
                return "ARRAY_INT"
            case FeatureTypes.array_float:
                return "ARRAY_FLOAT"
            case _:
                raise HttpError(
                    status_code=HTTPStatus.BAD_REQUEST.value,
                    message=f"The datatype: {datatype} is not allowed."
                )

    @classmethod
    def _update_feature_rows_with_new_feature(cls, feature_name: str, feature_store: FeatureStore) -> None:
        features_to_update = Features.objects.filter(feature_store=feature_store)
        rows_to_update = []
        for f in features_to_update:
            f.features[feature_name] = None
            rows_to_update.append(f)
        Features.objects.bulk_update(rows_to_update, ['features'], batch_size=500)

    @classmethod
    def feature_creation(cls, input: FeatureCreation) -> bool:
        # Make sure feature store exists
        feature_store = cls._check_feature_store(input.feature_store)
        with transaction.atomic():
            # create or update feature in metadata
            _, created = FeatureMetadata.objects.get_or_create(
                feature_name=input.feature_name,
                feature_store=feature_store,
                defaults={
                    "datatype": cls._match_datatype(input.datatype),
                    "feature_description": input.feature_description,
                    "data_source": input.data_source,
                }
            )
            # update existing JSON field for that feature store with new features
            cls._update_feature_rows_with_new_feature(input.feature_name, feature_store)
            return created

    @classmethod
    def feature_store_creation(cls, input: FeatureStoreCreation) -> bool:
        _, created = FeatureStore.objects.get_or_create(
            feature_store_name=input.store_name,
            defaults={
                "description": input.description
            }
        )
        return created

    @classmethod
    def _check_datatypes(cls, feature_data: Dict[str, Feature], feature_store: FeatureStore) -> None:
        feature_names = list(feature_data.keys())
        feature_metadata = FeatureMetadata.objects.filter(
            feature_name__in=feature_names,
            feature_store=feature_store
        )
        if not feature_metadata:
            raise HttpError(
                status_code=HTTPStatus.BAD_REQUEST.value,
                message=f"Feature metadata for keys passed in not found."
            )
        checker = {
            feature.feature_name: feature for feature in feature_metadata
        }
        for key, value in feature_data.items():
            datatype_info = checker[key]
            datatype = cls._match_db_datatype_to_python_datatype(datatype_info.datatype)
            if not isinstance(value, datatype):
                raise HttpError(
                    status_code=HTTPStatus.BAD_REQUEST.value,
                    message=f"A value of {value} was passed in for {key}, but key only accepts type {datatype}."
                )

    @classmethod
    def _feature_data_check(cls, input: FeatureDataUpload) -> FeatureStore:
        if not input.feature_store or not input.values:
            return
        # Make sure feature store exists
        feature_store = cls._check_feature_store(input.feature_store)
        # check datatypes
        cls._check_datatypes(input.values, feature_store)
        return feature_store

    @classmethod
    def upload_feature(cls, input: FeatureDataUpload) -> None:
        feature_store = cls._feature_data_check(input=input)
        # upload or create feature value
        Features.objects.update_or_create(
            feature_store=feature_store,
            entity_id=input.entity_id,
            defaults={"features": {**input.values}}
        )

    @classmethod
    def _parse_feature_fetch(cls, input: FetchFormat) -> FeatureFetchResponseData:
        feature_store = cls._check_feature_store(input.feature_store)
        values = Features.objects.filter(feature_store=feature_store, entity_id__in=input.entity_ids)
        ret = []
        # parse out json features from values
        for v in values:
            d = {
                feature: v.features[feature] for feature in input.features
                if feature in v.features
            }
            ret.append({
                'entity_id': v.entity_id,
                **d
            })
        return FeatureFetchResponseData(table=input.feature_store, data=ret)

    @classmethod
    def fetch(cls, input: FetchFeatures) -> FeatureFetchResponse:
        ret = []
        for fetchable in input.fetchables:
            ret.append(
                cls._parse_feature_fetch(fetchable)
            )
        return FeatureFetchResponse(data=ret)
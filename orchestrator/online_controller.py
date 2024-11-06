import json

from http import HTTPStatus
from django.utils import timezone
from ninja.errors import HttpError

from feature_logger.controller import FeatureLoggerService
from feature_logger.types import FeatureLogT
from feature_service.types import FetchFeatures, FetchFormat, FeatureFetchResponse
from feature_service.controller import FeatureService
from ml_model_registry.models import ModelMetadata
from orchestrator.types import *
from orchestrator.model_caller_controller import *


class OnlineOrcha:

    @classmethod
    def _get_model_caller_for_type(cls, model_type: str, feature_data: FeatureFetchResponse) -> MLModelCaller:
        match model_type:
            case "TENSORFLOW":
                return TensorflowModelCaller(features=feature_data)
            case "PYTORCH":
                return PytorchModelCaller(features=feature_data)
            case "SCIKIT":
                return ScikitModelCaller(features=feature_data)

    @classmethod
    def call_ml_model(cls, feature_data: FeatureFetchResponse, model: ModelMetadata) -> ModelResponseT:
        try:
            model_caller = cls._get_model_caller_for_type(model_type=model.model_type, feature_data=feature_data)
            features = model_caller.format_features()
            response = model_caller.serve(features=features)
            return ModelResponseT(response_object={"result": response})
        except Exception as e:
            return ModelResponseT(error_object={"error": f"error during processing {e}"})

    @classmethod
    def retrieve(cls, prompt: RetreivalT) -> RetreivalResponseT:
        # Check from cache when enabled
        if prompt.caching:
            # encode input as SHA and fetch from cache
            cls._check_cache()
        # fetch feature columns from model
        model = ModelMetadata.objects.filter(model_name=prompt.ml_model_name).first()
        if not model:
            raise HttpError(
                status_code=HTTPStatus.BAD_REQUEST.value,
                message=f"ML Model: {prompt.ml_model_name} is not register in ModelMetadata table."
            )
        # fetch features
        feature_data = []
        for feature_store, features in model.feature_set.items():
            if not (ent_ids := prompt.entity_ids.get(feature_store)):
                continue
            feature_data.append(
                FetchFormat(
                    feature_store=feature_store,
                    features=features,
                    entity_ids=ent_ids
                )
            )
        finalized_features = FetchFeatures(fetchables=feature_data)
        feature_results = FeatureService.fetch(finalized_features)
        # send to model
        result = cls.call_ml_model(feature_results, model)
        result_time = timezone.now()
        # Cache response when enabled
        if prompt.caching:
            # encode input as SHA and store as string in cache
            cls._store_cache()
        # log model response
        if prompt.log_response:
            log = FeatureLogT(
                data={
                    "model_response": result,
                    "result_time": result_time,
                    "features": finalized_features
                }
            )
            FeatureLoggerService.log(log)
        # return model response
        return RetreivalResponseT(
            ml_model_name=prompt.ml_model_name,
            response_object=result,
            result_time=result_time
        )

    @classmethod
    def _check_cache(cls, log: FeatureLogT):
        pass

    @classmethod
    def _store_cache(cls, log: ModelResponseT):
        pass